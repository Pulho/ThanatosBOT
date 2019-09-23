import discord
from config.setup  import bot

@bot.event
async def on_member_remove(member):
	print(f'{member} has left a server.')
