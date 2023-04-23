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
from app import *

class tagger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(
        name="imagetagger",
        description="gets the tags for an image",
    )
    async def imagetagger(
        self,
        interaction: Interaction
    ):
        image = await interaction.response.send_message(
            "Please send an image (max size: `8mb`)")
        try:
            message = await bot.wait_for(
                'message',
                check=lambda m:
                m.author == interaction.user
                and
                m.channel == interaction.channel,
                timeout = 20)
        except asyncio.TimeoutError:
            await image.edit(content="Sorry, you didn't send an image in time.")
            return
        
        await interaction.channel.send("Just a moment...")
        attachment = message.attachments[0]
        file_path = "image.png"
        await attachment.save(file_path)

        with open(file_path, "rb") as img_file:
            img_data = img_file.read()

        img64 = base64.b64encode(img_data).decode("ascii")

        tagger_payload = {
            "image": img64,
            "model": "wd14-vit-v2-git",
            "threshold": 0.35,
        }

        response = requests.post(
            url=f'{url}/tagger/v1/interrogate', json=tagger_payload)
        r = response.json()
        
        tags1 = []
        tags2 = []
        tags3 = []
        for tag, value in r['caption'].items():
            if len(tags1) < 10:
                tags1.append(f"{tag}: {'`{:.2%}`'.format(value)}\n")
            elif len(tags2) < 10:
                tags2.append(f"{tag}: {'`{:.2%}`'.format(value)}\n")
            else:
                tags3.append(f"{tag}: {'`{:.2%}`'.format(value)}\n")
        tags_str1 = "".join(tags1)
        tags_str2 = "".join(tags2)
        tags_str3 = "".join(tags3)

        embed = nextcord.Embed(
            title="Image Tags",
            color=nextcord.Color.green()
        )
        embed.add_field(name="Tags 1", value=tags_str1)
        embed.add_field(name="Tags 2", value=tags_str2)
        embed.add_field(name="Tags 3", value=tags_str3)
        file = nextcord.File("image.png")
        embed.set_image(url="attachment://image.png")
        await interaction.channel.send(embed = embed, file = file)

def setup(bot):
    bot.add_cog(tagger(bot)) 