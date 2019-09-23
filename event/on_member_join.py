import discord
from config.setup  import bot

@bot.event
async def on_member_join(member):
	print(f'{member} has joined a server.')
