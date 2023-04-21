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
token = "MTAzNjE4ODg2MDczODE5MTQxMg.GZYdOv.rEc9RDedDq1hJl0QfJAWwaSOtNLYul8Z08eELk"
response = {}

intents = nextcord.Intents.default()
intents.message_content = True

bot=commands.Bot(command_prefix="!", intents=nextcord.Intents.all())
client = commands.Bot()

serverID= 610478314506944512 
serverID2= 757893356746702928
serverID3= 1007818536636395600

class samplers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(
        name= "samplers",
        description= "get a list of samplers for tex2img",
        guild_ids=[serverID, serverID2, serverID3]
    )
    async def samplers(
        self,
        interaction : Interaction
    ):
        response = requests.get(url=f'{url}/sdapi/v1/samplers')
        if response.status_code == 200:
            samplers = response.json()
        for sampler in samplers:
            print(f"Sampler name: {sampler['name']}")
            if len(sampler['aliases']) > 0:
                print(f"Aliases: {', '.join(sampler['aliases'])}")
            print()

        sample = nextcord.Embed(title="Sampler List:")
        for i in range(0, len(samplers), 2):
            left_sampler = samplers[i]
            left_name = left_sampler['name']
            left_aliases = ", ".join(left_sampler['aliases'])

            right_sampler = None
            right_name = ""
            right_aliases = ""
            if i+1 < len(samplers):
                right_sampler = samplers[i+1]
                right_name = right_sampler['name']
                right_aliases = ", ".join(right_sampler['aliases'])

            sample.add_field(name=left_name, value=f"Aliases: `{left_aliases}`", inline=True)
            if right_sampler is not None:
                sample.add_field(name=right_name, value=f"Aliases: `{right_aliases}`", inline=True)

        await interaction.response.send_message(embed=sample)
def setup(bot):
    bot.add_cog(samplers(bot))