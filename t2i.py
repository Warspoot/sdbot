import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "https://c468ac617004e181d1.gradio.live"
option_payload = {
    "sd_model_checkpoint": "grapefruitv4.safetensors",
    "CLIP_stop_at_last_layers": 2
}
response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)

prompt= """masterpiece, best quality, highres, ((ultra-detailed)), ((cinematic lighting)), (illustration), ((beautiful detailed eyes)), depth of field, clear 8k wallpaper,
outside, suburban streets, snowing, walking, wind blowing,
(1girl), looking at viewer, medium breasts, very long hair, silver hair, purple eyes, (double hair bun), white underbust, black jacket, lavender skirt, hair bow ribbon, white beret, hair ornament, pink hair flower, mature, arms up,
happy, >3< , blush"""
negative_prompt= """lowres, bad anatomy, bad hands, text, error, missing fingers, extra digit, fewer digits, cropped, worst quality, low quality, normal quality, jpeg artifacts, signature, watermark, username, blurry, artist name, EasyNegative, Deep Negative V175,"""

payload = {
    "prompt": (prompt),
    "negative_prompt": (negative_prompt),
    "steps": 5,
    "cfg_scale": 7,
    "sampler_index": "Euler",
    "width": 700,
    "height": 500,
    "seed": -1,
}

response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

r = response.json()

for i in r['images']:
    image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

    png_payload = {
        "image": "data:image/png;base64," + i
    }
    response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

    pnginfo = PngImagePlugin.PngInfo()
    pnginfo.add_text("parameters", response2.json().get("info"))
    image.save('output.png', pnginfo=pnginfo)