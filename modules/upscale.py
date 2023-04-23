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

class upscalecmd(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @bot.slash_command(
        name="upscale",
        description="Upscale your images",
        guild_ids=[serverID, serverID2, serverID3]
    )
    async def upscale(
        self,
        interaction: Interaction, 
        scale : int, ):
        image = await interaction.response.send_message("Please send an image file")
        message = await bot.wait_for(
        'message',
            check=lambda m:
            m.author == interaction.user 
            and 
            m.channel == interaction.channel)
        await interaction.channel.send("Just a moment...")
        attachment = message.attachments[0]
        file_path = "Images/image.png" # Specify a file path here
        await attachment.save(file_path)  # Pass the file path argument to the save() method

        output = replicate.run(
            "xinntao/realesrgan:1b976a4d456ed9e4d1a846597b7614e79eadad3032e9124fa63859db0fd59b56",
            input= {"img" : open(file_path, "rb"),
                    "scale" : (scale)
                    }
        )
        urllib.request.urlretrieve((output),"Images/output.png")
        file = nextcord.File("Images/output.png")
        await interaction.channel.send(f"{(interaction.user.mention)} Here is the upscaled image:")
        await interaction.channel.send(file=file)
def setup(bot):
    bot.add_cog(upscalecmd(bot))