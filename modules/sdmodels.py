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

url = "https://f1210f2c7080ee8889.gradio.live/"
response = {}

intents = nextcord.Intents.default()
intents.message_content = True

bot=commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
client = commands.Bot()

serverID= 610478314506944512 
serverID2= 757893356746702928
serverID3= 1007818536636395600

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
        model_names = model_names = "\n".join(title['title'] for title in models)

        model_list = nextcord.Embed(
            title="Checkpoint Model List:",
            description=f"`{model_names}\n`"
        )
        await interaction.response.send_message(embed=model_list)
def setup(bot):
    bot.add_cog(sdmodels(bot))