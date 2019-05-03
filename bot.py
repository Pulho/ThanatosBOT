import discord
from commands import *
from setup import __prefix__, __token__
from discord.ext import commands

bot = commands.Bot(command_prefix = __prefix__)

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name='Type !Help for more'))
	print('Bot is Ready')

@bot.event
async def on_member_join(member):
	print(f'{member} has joined a server.')

@bot.event
async def on_member_remove(member):
	print(f'{member} has left a server.')
bot.run(__token__)