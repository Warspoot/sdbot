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

class setmodel(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(
        name= "setmodel",
        description="sets the checkpoint model used for generation",
        guild_ids=[serverID, serverID2, serverID3]
    )
    async def setmodel(
        self,
        interaction : Interaction,
        model : str
        ):
        await interaction.response.send_message("Just a moment...")

        global option_payload 
        option_payload = {
        "sd_model_checkpoint": (model),
        }

        print(option_payload)
        await interaction.channel.send(f"Successfully set Model! \n The model is now: **{str(model)}**")

        global response
        response = requests.post(url=f'{url}/sdapi/v1/options', json=option_payload)
def setup(bot):
    bot.add_cog(setmodel(bot))