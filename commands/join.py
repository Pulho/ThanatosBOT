import discord
from commands import *
from discord.ext import commands

@bot.command(pass_context=True)
async def join(context):
	channel = context.author.voice.voice_channel
	await bot.join_voice_channel(channel)