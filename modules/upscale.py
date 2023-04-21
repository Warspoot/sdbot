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

os.environ["REPLICATE_API_TOKEN"] = "11e735e40d36e12c1ad1dbd322e288f793c820c0"
token = "MTAzNjE4ODg2MDczODE5MTQxMg.GZYdOv.rEc9RDedDq1hJl0QfJAWwaSOtNLYul8Z08eELk"
response = {}

intents = nextcord.Intents.default()
intents.message_content = True

bot=commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
client = commands.Bot()

serverID= 610478314506944512 
serverID2= 757893356746702928
serverID3= 1007818536636395600

class upscale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(
    name="upscale",
    description="Upscale your images",
    guild_ids=[serverID, serverID2, serverID3]
    )
    async def upscale(
            self,
            interaction: Interaction,
            scale : int,
            ):
        image = await interaction.response.send_message("Please send an image file")
        message = await bot.wait_for(
        'message',
            check=lambda m:
            m.author == interaction.user 
            and 
            m.channel == interaction.channel)
        
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
        await interaction.channel.send("Here is the upscaled image:")
        await interaction.channel.send(file=file)
def setup(bot):
    bot.add_cog(upscale(bot))