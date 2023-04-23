import nextcord
import replicate
import os
import urllib.request
import json
import requests
import io
import base64
import asyncio
from nextcord import Interaction
from nextcord.ext import commands
from PIL import Image, PngImagePlugin

#import url and tokens from env.py
from env import *
os.environ["REPLICATE_API_TOKEN"] = replicate_token
url = sd_url
token = discord_token
response = {}

intents = nextcord.Intents.default()
intents.message_content = True

bot=commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
client = commands.Bot()

serverID= 610478314506944512 
serverID2= 757893356746702928
serverID3= 1007818536636395600

@bot.event
async def on_ready():
    print(f"Bot is ready!")
    # await schedule_daily_message()
    await bot.change_presence(activity=nextcord.Game(name="Stable Diffusion"))

bot.load_extension('modules.set_settings')

bot.load_extension('modules.samplers')

bot.load_extension('modules.sdmodels')

bot.load_extension('modules.setmodel')

bot.load_extension('modules.setclipskip')

bot.load_extension('modules.setvae')

bot.load_extension('modules.getsettings')

bot.load_extension('modules.upscale')

@bot.slash_command(
    name= "text2image",
    description="creates an image from input prompts",
    guild_ids=[serverID, serverID2, serverID3]
)
async def t2img(
    interaction : Interaction,
    prompt : str,
    negative : str,
    steps: int,
    sampler: str,
    cfg: int,
    width : int,
    height : int
    ):
    SeedAsk = await interaction.response.send_message("Would you like to use a set seed or random?")
    message = await bot.wait_for(
       'message',
         check=lambda m:
           m.author == interaction.user 
           and 
           m.channel == interaction.channel)
    sseed= message.content 
    if message.content == "" or "r" or "random" or "default":
        sseed = -1
    else:
        sseed = message.content

    await interaction.channel.send("Just a moment...")

    payload = {
    "prompt": (prompt),
    "negative_prompt": (negative),
    "steps": (steps),
    "cfg_scale": (cfg),
    "sampler_index": (sampler),
    "width": (width),
    "height": (height),
    "seed": (sseed),
}
    print(prompt)
    print(negative)
    print(steps)
    print(cfg)
    print(sampler)
    print(width)
    print(height)
    global response

    while True:
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
        png_data = response2.json().get("info")
        png_data_list = png_data.split("\n")
        print(png_data_list)
        extra_params_split = png_data_list[2].split(", ")
        for line in extra_params_split:
                if 'Model hash: ' in line:
                    model_hash = line.split(': ', 1)[1]
                if 'Model: ' in line:
                    model_name = line.split(': ', 1)[1]

                if 'Steps: ' in line:
                    steps = line.split(': ', 1)[1]
                if 'Size: ' in line:
                    size = line.split(': ', 1)[1]
                if 'CFG scale: ' in line:
                    guidance_scale = line.split(': ', 1)[1]
                if 'Sampler: ' in line:
                    sampler = line.split(': ', 1)[1]
                if 'Seed: ' in line:
                    seed = line.split(': ', 1)[1]
        print(seed)
        image.save(f'SDImages/{interaction.user} - {seed}.png', pnginfo=pnginfo)
        image.save('output.png', pnginfo=pnginfo)
        
        Embed = nextcord.Embed(
            title = "Image Info",
            description= f"Generated by: `{interaction.user}`, \n Model: `{str(model_name)}` \n Sampler: `{str(sampler)}` CFG Scale: `{str(guidance_scale)}` \n Size: `{str(size)}` \n Seed: `{str(seed)}` Steps: `{(steps)}` \n You've got 60 seconds to reroll"
        )
        file = nextcord.File("output.png")
        Embed.set_image(url="attachment://output.png")
        sent_embed = await interaction.followup.send(embed = Embed, file = file)
        await sent_embed.add_reaction("<:moment:1009375804423147560>")
        
        #if reaction is reacted, then repeat the code again
        def check(reaction: nextcord.Reaction, user: nextcord.User):
            return (
                user == interaction.user
                and str(reaction.emoji) == "<:moment:1009375804423147560>"
                and reaction.message.id == sent_embed.id
            )
        try:
            reaction, user = await bot.wait_for(
                "reaction_add",
                timeout=80.0,
                check=check
            )
            await interaction.channel.send("Rerolling...")
        except asyncio.TimeoutError:
            await message.remove_reaction("<:moment:1009375804423147560>", bot.user)
            await message.add_reaction("<a:tenor5:847460229780209734>")
            await interaction.channel.send("Timed out.")
            break

bot.run(token)