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

vae_if = "nai.vae.pt" or "orangemix.vae.pt" or "none" or "Automatic"
vae_list = "`nai.vae.pt` or `orangemix.vae.pt` or `none` or `Automatic`"
class setvae(commands.Cog):
    def __init__ (self, bot):
        self.bot = bot

    @bot.slash_command(
        name = "setvae",
        description = "set vae for image generation",
        guild_ids=[serverID, serverID2, serverID3]
    )
    async def definevae(
        self,
        interaction : Interaction,
        vae : str,
        ):
        if vae != vae_if:
            vae = "Automatic"
            await interaction.channel.send("Invalid VAE! Setting VAE to Automatic")

        await interaction.response.send_message("Just a moment...")
        global option_payload
        option_payload = {
            "sd_vae" : (vae),
        }
        print(option_payload)
        print(vae)

        global response
        response = requests.post(url=f'{url}/sdapi/v1/options', json = option_payload)
        await interaction.followup.send(f"VAE has been set (if invalid VAE was given then VAE is set to Audomatic)")
def setup(bot):
    bot.add_cog(setvae(bot))