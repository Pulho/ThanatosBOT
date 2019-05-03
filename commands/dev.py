import discord
from commands import *
from discord.ext import commands

@bot.command(pass_context=True)
async def dev(context):
	await context.send('Actual developer: Pulho (https://github.com/Pulho)')
