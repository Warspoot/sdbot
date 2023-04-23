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

class getset(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(
        name = "getsettings",
        description = "get a list of the current settings",
        guild_ids=[serverID, serverID2, serverID3]
    )
    async def getsettings(
        self,
        interaction : Interaction
    ):
        response = requests.get(url=f'{url}/sdapi/v1/options')
        if response.status_code == 200:
            settings = response.json()
            print(settings)
            clipskip = settings["CLIP_stop_at_last_layers"]
            vae = settings["sd_vae"]
            print(clipskip)
        model_list = nextcord.Embed(
            title="Setting List:",
            description=f"Clipskip: `{clipskip}\n` Vae: `{vae}`"
        )
        await interaction.response.send_message(embed=model_list)
def setup(bot):
    bot.add_cog(getset(bot))