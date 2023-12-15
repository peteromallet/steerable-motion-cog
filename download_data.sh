cd ComfyUI
# loading custom nodes
# git clone https://github.com/Kosinkadink/ComfyUI-AnimateDiff.git custom_nodes/ComfyUI-AnimateDiff
# git clone https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet.git custom_nodes/ComfyUI-Advanced-ControlNet

# loading motion module
wget -c https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v14.ckpt -P ./custom_nodes/ComfyUI-AnimateDiff/models/
wget -c https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15.ckpt -P ./custom_nodes/ComfyUI-AnimateDiff/models/
wget -c https://huggingface.co/guoyww/animatediff/resolve/main/mm_sd_v15_v2.ckpt -P ./custom_nodes/ComfyUI-AnimateDiff/models/

# loading models/ vae/ controlnet
wget -c https://huggingface.co/SG161222/Realistic_Vision_V5.0_noVAE/resolve/main/Realistic_Vision_V5.0.safetensors -P ./models/checkpoints/
wget -c https://huggingface.co/gsdf/Counterfeit-V3.0/resolve/main/Counterfeit-V3.0_fp32.safetensors -P ./models/checkpoints/
wget -c https://civitai.com/api/download/models/134065 -P ./models/checkpoints/
mv ./models/checkpoints/134065 ./models/checkpoints/epic_realism.safetensors
wget -c https://civitai.com/api/download/models/128713 -P ./models/checkpoints/
mv ./models/checkpoints/128713 ./models/checkpoints/dreamshaper_v8.safetensors
wget -c https://civitai.com/api/download/models/156110 -P ./models/checkpoints/
mv ./models/checkpoints/156110 ./models/checkpoints/deliberate_v3.safetensors


wget -c https://huggingface.co/stabilityai/sd-vae-ft-mse-original/resolve/main/vae-ft-mse-840000-ema-pruned.safetensors -P ./models/vae/
wget -c https://huggingface.co/lllyasviel/ControlNet-v1-1/resolve/main/control_v11f1e_sd15_tile.pth -P ./models/controlnet/
wget -c https://huggingface.co/comfyanonymous/GLIGEN_pruned_safetensors/resolve/main/gligen_sd14_textbox_pruned_fp16.safetensors -P ./models/gligen/
