import subprocess
import threading
import time
from cog import BasePredictor, Input, Path
import os
import shutil
import uuid
import json
import urllib
import websocket
from PIL import Image
from urllib.error import URLError
import random


class Predictor(BasePredictor):
    def setup(self):
        # start server
        self.server_address = "127.0.0.1:8188"
        self.start_server()

    def start_server(self):
        server_thread = threading.Thread(target=self.run_server)
        server_thread.start()

        while not self.is_server_running():
            time.sleep(1)  # Wait for 1 second before checking again

        print("Server is up and running!")

    def run_server(self):
        command = "python ./ComfyUI/main.py"
        server_process = subprocess.Popen(command, shell=True)
        server_process.wait()

    # hacky solution, will fix later
    def is_server_running(self):
        try:
            with urllib.request.urlopen("http://{}/history/{}".format(self.server_address, "123")) as response:
                return response.status == 200
        except URLError:
            return False

    def _copy_images_in_AD_repo(self, **kwargs):
        destination_folder = "./ComfyUI/input/"

        res = []
        for k, v in kwargs.items():
            staring_filename = os.path.basename(v)
            destination_path = os.path.join(destination_folder, staring_filename)
            shutil.copy(v, destination_path)
            res.append(staring_filename)
        
        print('final res: ', res)
        return res[0], res[1], res[2]

    def queue_prompt(self, prompt, client_id):
            p = {"prompt": prompt, "client_id": client_id}
            data = json.dumps(p).encode('utf-8')
            req =  urllib.request.Request("http://{}/prompt".format(self.server_address), data=data)
            return json.loads(urllib.request.urlopen(req).read())

    def get_image(self, filename, subfolder, folder_type):
        data = {"filename": filename, "subfolder": subfolder, "type": folder_type}
        url_values = urllib.parse.urlencode(data)
        with urllib.request.urlopen("http://{}/view?{}".format(self.server_address, url_values)) as response:
            return response.read()

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
                print("node output: ", node_output)
                
                if 'gifs' in node_output:
                    for gif in node_output['gifs']:
                        output_gifs.append(gif['filename'])

        return output_gifs
    
    # TODO: add dynamic fields based on the workflow selected
    def predict(
        self,
        prompt_travel: str = Input(description="Prompt travel", default="0_:16_:24_"),
        negative_prompt: str = Input(description="Negative Prompt", default="(worst quality, low quality:1.2)"),
        image_dimension: str = Input(
            description="Select image dimenstions",
            default="512x512",
            choices=[
                "512x512",
                "512x768",
                "768x512"
            ],
        ),
        img_1: Path = Input(description="Image 1"),
        img_2: Path = Input(description="Image 2"),
        img_3: Path = Input(description="Image 3"),
        motion_module: str = Input(
            description="Select a Motion Model",
            default="mm_sd_v14.ckpt",
            choices=[
                "mm_sd_v14.ckpt",
                "mm_sd_v15_v2.ckpt"
            ],
        ),
        model: str = Input(
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
        img_1_latent_cn_weights: str = Input(
            default="0=1.00,1=0.82,2=0.74,3=0.56,4=0.47,5=0.41,6=0.38,7=0.33,8=0.30,9=0.28,10=0.25,11=0.24,12=0.20,13=0.17,14=0.15,15=0.13,16=0.13,17=0.11,18=0.11,19=0.11,20=0.11,21=0.11,22=0.10,23=0.09,24=0.06,25=0.04,26=0.03,27=0.01,28=0.00,29=0.00,30=0.00,31=0.00,32=0.00,33=0.00,34=0.00,35=0.00,36=0.00,37=0.00,38=0.00,39=0.00,40=0.00,41=0.00,42=0.00,43=0.00,44=0.00,45=0.00,46=0.00,47=0.00",
            description="weights for how cn will affect the latents"
        ),
        img_2_latent_cn_weights: str = Input(
            default="0=0.09,1=0.10,2=0.11,3=0.11,4=0.11,5=0.11,6=0.11,7=0.13,8=0.13,9=0.15,10=0.17,11=0.20,12=0.24,13=0.25,14=0.28,15=0.30,16=0.33,17=0.38,18=0.41,19=0.47,20=0.56,21=0.74,22=0.82,23=1.00,24=1.00,25=0.82,26=0.74,27=0.56,28=0.47,29=0.41,30=0.38,31=0.33,32=0.30,33=0.28,34=0.25,35=0.24,36=0.20,37=0.17,38=0.15,39=0.13,40=0.13,41=0.11,42=0.11,43=0.11,44=0.11,45=0.11,46=0.10,47=0.09\n\n\n\n",
            description="weights for how cn will affect the latents"
        ),
        img_3_latent_cn_weights: str = Input(
            default="0=0.00,1=0.00,2=0.00,3=0.00,4=0.00,5=0.00,6=0.00,7=0.00,8=0.00,9=0.00,10=0.00,11=0.00,12=0.00,13=0.00,14=0.00,15=0.00,16=0.00,17=0.00,18=0.00,19=0.00,20=0.01,21=0.03,22=0.04,23=0.06,24=0.09,25=0.10,26=0.11,27=0.11,28=0.11,29=0.11,30=0.11,31=0.13,32=0.13,33=0.15,34=0.17,35=0.20,36=0.24,37=0.25,38=0.28,39=0.30,40=0.33,41=0.38,42=0.41,43=0.47,44=0.56,45=0.74,46=0.82,47=1.00",
            description="weights for how cn will affect the latents"
        ),
        ip_adapter_weight: float = Input(default=0.4, description="IPAdapter weight"),
        ip_adapter_noise: float = Input(default=0.5, description="IPAdapter noise"),
        output_format: str = Input(
            default="video/h264-mp4",
            choices=[
                "video/h264-mp4",
                "image/gif"
            ],
            description="Output format",
        ),
    ) -> Path:

        video_output_path = self.get_workflow(
            prompt_travel=prompt_travel,
            negative_prompt=negative_prompt,
            img_1=img_1,
            img_2=img_2,
            img_3=img_3,
            motion_module=motion_module,
            model=model,
            img_1_latent_cn_weights=img_1_latent_cn_weights,
            img_2_latent_cn_weights=img_2_latent_cn_weights,
            img_3_latent_cn_weights=img_3_latent_cn_weights,
            ip_adapter_weight=ip_adapter_weight,
            ip_adapter_noise=ip_adapter_noise,
            output_format=output_format,
            image_dimension=image_dimension
        )
            
        return Path(video_output_path)
    
    def get_workflow(self, **args):
        # copy img inside comfy
        img_1, img_2, img_3 = self._copy_images_in_AD_repo(
            img_1=args['img_1'], img_2=args['img_2'], img_3=args['img_3'])

        # load config
        prompt = None
        workflow_config = "./custom_workflows/workflow_pom.json"

        with open(workflow_config, 'r') as file:
            prompt = json.load(file)

        if not prompt:
            raise Exception('no workflow config found')

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

        return './ComfyUI/output/AnimateDiff/' + gif_list[0]