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

url = "https://0a5fb73816cc7be3ae.gradio.live"
response = {}

intents = nextcord.Intents.default()
intents.message_content = True

bot=commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
client = commands.Bot()

serverID= 610478314506944512 
serverID2= 757893356746702928
serverID3= 1007818536636395600

class Mycog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(
        name= "settings",
        description="settings for ai generation",
        guild_ids=[serverID, serverID2, serverID3]
    )
    async def settings(
        self,
        interaction : Interaction,
        model : str,
        clip : int,
        ):
        await interaction.channel.send("Just a moment...")
        await interaction.response.defer()

        global option_payload 
        option_payload = {
        "sd_model_checkpoint": (model),
        "CLIP_stop_at_last_layers": (clip)
        }

        print(option_payload)
        await interaction.channel.send(f"Successfully set settings! \n The model is now: **{str(model)}** \n The clip skip is now: **{int(clip)}**")

        global response
        response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)
def setup(bot):
    bot.add_cog(Mycog(bot))