import discord
import asyncio
import os
import pafy
import random
import ffmpy
from youtube_dl import YoutubeDL
from commands import *
from discord.voice_client import VoiceClient
from discord.ext import commands

__prefix__ = '!'
__token__ = 'NDA4NjU2ODk2NDk3NTQ5MzEy.DVTO7w.3SKVdlK6_1OLI8Jx0u7-UHIGpFY'

bot = commands.Bot(command_prefix = __prefix__)