import subprocess
import threading
import time

import psutil
from cog import BasePredictor, Input, Path
import os
import shutil
import uuid
import json
import urllib
import websocket
import zipfile
from PIL import Image
from urllib.error import URLError
import random


class Predictor(BasePredictor):
    def setup(self):
        # start server
        self.server_address = "127.0.0.1:8188"
        self.server_thread = None
        self.server_process = None

    def start_server(self):
        # self.server_thread = threading.Thread(target=self.run_server)
        # self.server_thread.start()
        self.run_server()

        while not self.is_server_running():
            time.sleep(1)  # Wait for 1 second before checking again

        print("Server is up and running!")

    def find_and_kill_process_by_port(self, port):
        for proc in psutil.process_iter(attrs=['pid', 'name', 'connections']):
            try:
                if proc and 'connections' in proc.info and proc.info['connections']:
                    for conn in proc.info['connections']:
                        if conn.status == psutil.CONN_LISTEN and conn.laddr.port == port:
                            print(f"Killing process {proc.info['pid']} (Port {port})")
                            psutil.Process(proc.info['pid']).terminate()
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

    def run_server(self):
        command = "python ./ComfyUI/main.py"
        self.server_process = subprocess.Popen(command, shell=True)
        # self.server_process.wait()

    # hacky solution, will fix later
    def is_server_running(self):
        try:
            with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, "123")) as response:
                return response.status == 200
        except Exception as e:
            return False

    def _copy_images_in_AD_repo(self, *args):
        current_directory = os.getcwd()
        print("Current Working Directory:", current_directory)

        destination_folder = "./ComfyUI/input/images"
        if not os.path.exists(destination_folder):
            os.makedirs(destination_folder)
            
        res = []

        for filepath in args:
            filename = os.path.basename(filepath)
            destination_path = os.path.join(destination_folder, filename)
            shutil.copy(filepath, destination_path)
            res.append(filename)
            print("copying file: ", filename, destination_folder)
        
        return res

    def queue_prompt(self, prompt, client_id):
            p = {"prompt": prompt, "client_id": client_id}
            data = json.dumps(p).encode('utf-8')
            req =  urllib.request.Request("http://{}/prompt".format(self.server_address), data=data)
            return json.loads(urllib.request.urlopen(req).read())

    def get_history(self, prompt_id):
        with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, prompt_id)) as response:
            return json.loads(response.read())

    def get_gifs(self, ws, prompt, client_id):
        prompt_id = self.queue_prompt(prompt, client_id)['prompt_id']
        while True:
            out = ws.recv()
            if isinstance(out, str):
                message = json.loads(out)
                if message['type'] == 'executing':
                    data = message['data']
                    if data['node'] is None and data['prompt_id'] == prompt_id:
                        break #Execution is done
            else:
                continue #previews are binary data

        history = self.get_history(prompt_id)[prompt_id]
        output_gifs = []
        for o in history['outputs']:
            for node_id in history['outputs']:
                node_output = history['outputs'][node_id]
                # print("node output: ", node_output)
                
                if 'gifs' in node_output:
                    for gif in node_output['gifs']:
                        output_gifs.append(gif['filename'])

        return output_gifs
    
    # TODO: add dynamic fields based on the workflow selected
    def predict(
        self,
        # input images + batchprompt
        image_list: Path = Input(description="Image list (.zip file)"),
        image_prompt_list: str = Input(description="Image prompt list", default="0_:16_:24_:36_:48_:60_:72_:84_:96_:108_"),
        negative_prompt: str = Input(description="Negative Prompt", default="(worst quality, low quality:1.2)"),
        
        # creative interpolation
        type_of_frame_distribution: str = Input(
            default="linear",
            choices=["linear", "dynamic"],
            description="Frame distribution",
        ),
        linear_frame_distribution_value: int = Input(description='Linear Frames per keyframe', default=16),
        dynamic_frame_distribution_values: str = Input(description='Dynamic Frames per keyframe', default="0,10,26,40,46"),
        type_of_key_frame_influence: str = Input(
            default="linear",
            choices=["linear", "dynamic"],
            description="Frame distribution",
        ),
        linear_key_frame_influence_value: float = Input(description='Linear keyframe influence', default=0.9),
        dynamic_key_frame_influence_values: str = Input(description='Dynamic keyframe influence', default="0.5,0.5,2.0,0.5"),
        buffer: int = Input(description='Buffer', default=4),
        type_of_cn_strength_distribution: str = Input(
            default="dynamic",
            choices=["linear", "dynamic"],
            description="Type of CN strength distribution",
        ),
        linear_cn_strength_value: str = Input(description='Linear CN strength influence', default="(0.0,1.0)"),
        dynamic_cn_strength_values: str = Input(description='Dynamic CN strength influence', default="(0.0,1.0),(0.0,1.0),(0.0,1.0),(0.0,1.0)"),

        soft_scaled_cn_weights_multiplier: float = Input(description='cn multiplier', default=0.87),
        stmfnet_multiplier: float = Input(description='stmfnet multiplier', default=2),

        # efficient loader (figure out batch-size)
        ckpt: str = Input(
            default="Counterfeit-V3.0_fp32.safetensors",
            choices=[
                "Realistic_Vision_V5.0.safetensors",
                "Counterfeit-V3.0_fp32.safetensors",
                "epic_realism.safetensors",
                "dreamshaper_v8.safetensors",
                "deliberate_v3.safetensors"
            ],
            description="Select a Module",
        ),

        # animate diff
        motion_scale: float = Input(description='Motion scale', default=0.8),

        # ip adapter weight
        relative_ipadapter_strength: float = Input(description='IP adapter image weight', default=1.0),
        relative_ipadapter_influence: float = Input(description='IP adapter image weight', default=1.0),
        ipadapter_noise: float = Input(description='IP adapter noise', default=0.0),
        image_dimension: str = Input(
            description="Select image dimenstions",
            default="512x512",
            choices=[
                "512x512",
                "512x768",
                "768x512"
            ],
        ),        
        output_format: str = Input(
            default="video/h264-mp4",
            choices=[
                "video/h264-mp4",
                "image/gif"
            ],
            description="Output format",
        ),
    ) -> Path:
        """Run a single prediction on the model"""
        self.find_and_kill_process_by_port(8188)
        self.start_server()

        # queue prompt
        video_output_path = self.get_workflow_output(
            image_list=image_list,
            image_prompt_list=image_prompt_list,
            negative_prompt=negative_prompt,
            type_of_frame_distribution=type_of_frame_distribution,
            linear_frame_distribution_value=linear_frame_distribution_value,
            dynamic_frame_distribution_values=dynamic_frame_distribution_values,
            type_of_key_frame_influence=type_of_key_frame_influence,
            linear_key_frame_influence_value=linear_key_frame_influence_value,
            dynamic_key_frame_influence_values=dynamic_key_frame_influence_values,
            type_of_cn_strength_distribution=type_of_cn_strength_distribution,
            linear_cn_strength_value=linear_cn_strength_value,
            buffer=buffer,
            dynamic_cn_strength_values=dynamic_cn_strength_values,            
            ckpt=ckpt,
            motion_scale=motion_scale,
            relative_ipadapter_strength=relative_ipadapter_strength,
            relative_ipadapter_influence=relative_ipadapter_influence,
            ipadapter_noise=ipadapter_noise,
            image_dimension=image_dimension,
            output_format=output_format,
            soft_scaled_cn_weights_multiplier=soft_scaled_cn_weights_multiplier,
            stmfnet_multiplier=stmfnet_multiplier
        )

        self.server_process.terminate()
        # deleting input folder (so that it doesn't affect subsequent runs)
        folder_to_delete = './ComfyUI/input/images'

        try:
            shutil.rmtree(folder_to_delete)
            print(f"The folder '{folder_to_delete}' has been successfully deleted.")
        except Exception as e:
            print(f"Error: {e}")

        # video_path = "./ComfyUI/output/creative_interpolation_results/AD__00002.mp4"
        print("************* final video output: ", video_output_path)
        return Path(video_output_path)
    
    def get_workflow_output(self, **kwargs):
        image_list = kwargs['image_list']
        image_prompt_list = kwargs['image_prompt_list']
        negative_prompt = kwargs['negative_prompt']
        type_of_frame_distribution = kwargs['type_of_frame_distribution']
        linear_frame_distribution_value = kwargs['linear_frame_distribution_value']
        dynamic_frame_distribution_values = kwargs['dynamic_frame_distribution_values']
        type_of_key_frame_influence = kwargs['type_of_key_frame_influence']
        linear_key_frame_influence_value = kwargs['linear_key_frame_influence_value']
        dynamic_key_frame_influence_values = kwargs['dynamic_key_frame_influence_values']
        type_of_cn_strength_distribution=kwargs['type_of_cn_strength_distribution']
        linear_cn_strength_value=kwargs['linear_cn_strength_value']
        buffer = kwargs['buffer']
        dynamic_cn_strength_values = kwargs['dynamic_cn_strength_values']
        ckpt = kwargs['ckpt']
        motion_scale = kwargs['motion_scale']
        relative_ipadapter_strength = kwargs['relative_ipadapter_strength']
        relative_ipadapter_influence = kwargs['relative_ipadapter_influence']
        ipadapter_noise = kwargs['ipadapter_noise']
        image_dimension = kwargs['image_dimension']
        output_format = kwargs['output_format']
        soft_scaled_cn_weights_multiplier = kwargs['soft_scaled_cn_weights_multiplier']
        stmfnet_multiplier = kwargs['stmfnet_multiplier']
        
        extracted_dir = os.path.dirname(image_list)
        extracted_file_paths = []
        with zipfile.ZipFile(image_list, 'r') as zip_ref:
            for file_info in zip_ref.infolist():
                if not file_info.filename.startswith('__MACOSX') and not file_info.filename.startswith('.DS_Store'):
                    print(file_info, " ---- ", file_info.filename)
                    zip_ref.extract(file_info, extracted_dir)
                    extracted_file_paths.append(os.path.join(extracted_dir, file_info.filename))
        
        # copy img inside comfy
        filename_list = self._copy_images_in_AD_repo(*extracted_file_paths)
        print("******** filename list: ", filename_list)
        if type_of_frame_distribution == 'linear':
            batch_size = (len(filename_list) - 1) * linear_frame_distribution_value + int(buffer)
        else:
            batch_size = int(dynamic_frame_distribution_values.split(',')[-1]) + int(buffer)

        print("batch size: ", batch_size)

        # load config
        prompt = None
        workflow_config = "./custom_workflows/workflow_pom.json"

        with open(workflow_config, 'r') as file:
            prompt = json.load(file)
        
        if not prompt:
            raise Exception('no workflow config found')
        

        

        # Assuming the base directory is known, for example, "~/ad_cog-main/ComfyUI/"
        base_directory = ""

        
        # Resolving the full path in case of relative paths or use of '~'
        # full_input_directory_path = os.path.expanduser(os.path.join(base_directory, 'input/images'))
        # prompt['401']['inputs']['directory'] = full_input_directory_path
        
        
        # prompt['401']['inputs']['directory'] = full_input_directory_path
        
        empty_latent_width, empty_latent_height = image_dimension.split("x")
        
        prompt["189"]["inputs"]["empty_latent_width"] = int(empty_latent_width)    
        prompt["189"]["inputs"]["empty_latent_height"] = int(empty_latent_height)                
        prompt["189"]["inputs"]["ckpt_name"] = ckpt            
        prompt["189"]["inputs"]["batch_size"] = batch_size                
        prompt["187"]["inputs"]["motion_scale"] = motion_scale            
        prompt["367"]["inputs"]["text"] = image_prompt_list            
        prompt["352"]["inputs"]["text"] = negative_prompt    
        prompt["437"]["inputs"]["type_of_frame_distribution"] = type_of_frame_distribution        
        prompt["437"]["inputs"]["linear_frame_distribution_value"] = linear_frame_distribution_value
        prompt["437"]["inputs"]["dynamic_frame_distribution_values"] = dynamic_frame_distribution_values            
        prompt["437"]["inputs"]["type_of_key_frame_influence"] = type_of_key_frame_influence            
        prompt["437"]["inputs"]["linear_key_frame_influence_value"] = linear_key_frame_influence_value            
        prompt["437"]["inputs"]["dynamic_key_frame_influence_values"] = dynamic_key_frame_influence_values            
        prompt["437"]["inputs"]["type_of_cn_strength_distribution"] = type_of_cn_strength_distribution            
        prompt["437"]["inputs"]["linear_cn_strength_value"] = linear_cn_strength_value            
        prompt["437"]["inputs"]["dynamic_cn_strength_values"] = dynamic_cn_strength_values            
        prompt["437"]["inputs"]["buffer"] = buffer                      
        prompt["437"]["inputs"]["soft_scaled_cn_weights_multiplier"] = soft_scaled_cn_weights_multiplier            
        prompt["437"]["inputs"]["relative_ipadapter_strength"] = relative_ipadapter_strength   
        prompt["437"]["inputs"]["relative_ipadapter_influence"] = relative_ipadapter_influence   
        prompt["437"]["inputs"]["ipadapter_noise"] = ipadapter_noise
        prompt["292"]["inputs"]["multiplier"] = stmfnet_multiplier             
        prompt["281"]["inputs"]["format"] = output_format        

        # start the process
        client_id = str(uuid.uuid4())
        ws = websocket.WebSocket()
        ws.connect("ws://{}/ws?clientId={}".format(self.server_address, client_id))
        gif_list = self.get_gifs(ws, prompt, client_id)

        # print("gif list: ", gif_list)
        return './ComfyUI/output/steerable-motion/' + gif_list[0] if gif_list and len(gif_list) else None