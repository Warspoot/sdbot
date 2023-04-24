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

class progress(commands.cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.slash_command(
        name= "progress",
        description= "check generation progress"
    )
    async def progress(
        self,
        interaction : Interaction
    ):
        