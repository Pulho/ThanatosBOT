import discord
from config.setup  import bot

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name='Type !Help for more'))
	print('Bot is Ready')
