import discord
from commands import *
from discord.ext import commands

@bot.command(pass_context=True)
async def ping(context):
	await context.send(f'Pong! {round(bot.latency * 1000)}ms')
