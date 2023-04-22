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

class sdmodels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(
        name = "models",
        description = "get a list of models to use for text2img",
        guild_ids=[serverID, serverID2, serverID3]
    )
    async def models(
        self,
        interaction : Interaction
    ):
        response = requests.get(url=f'{url}/sdapi/v1/sd-models')
        if response.status_code == 200:
            models = response.json()
            print(models)
        model_names = model_names = "\n".join(title['title'] for title in models)

        model_list = nextcord.Embed(
            title="Checkpoint Model List:",
            description=f"`{model_names}\n`"
        )
        await interaction.response.send_message(embed=model_list)
def setup(bot):
    bot.add_cog(sdmodels(bot))