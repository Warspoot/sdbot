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

class progress(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(
        name= "progress",
        description= "check generation progress"
    )
    async def getprogress(
        self,
        interaction : Interaction
    ):
        response = requests.get(url=f'{url}/sdapi/v1/progress')
        if response.status_code == 200:
            progress = response.json()
            print(progress)
        await interaction.response.send_message("printed to console.")
def setup(bot):
    bot.add_cog(progress(bot))