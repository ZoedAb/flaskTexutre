import base64
from diffusers import StableDiffusionPipeline
import torch
from io import BytesIO
MODEL_ID = "dream-textures/texture-diffusion"



# prompt = "brick wall"
# image = pipe(prompt).images[0]  
    
# image.save("bricks.png")

def generate(prompt):
    pipe = StableDiffusionPipeline.from_pretrained(MODEL_ID, torch_dtype=torch.float16)
    pipe = pipe.to("cpu")
    images_json = {}
    image = pipe(prompt).images[0]  
    buffered = BytesIO()
    image.save(buffered,format='PNG')
    #image.save("image.png")
    #print(image)
    base64_image = base64.b64encode(buffered.getvalue()).decode('utf-8')
    images_json["albedo"] = base64_image
    return images_json