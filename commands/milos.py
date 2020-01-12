import random
import discord
from config.setup  import bot

@bot.command()
async def oursecret(context):
	milosList = [
	'https://media.tenor.com/images/f93396356d12b6ed1b9c3c3627e2ddf4/tenor.gif',
	'https://media1.tenor.com/images/b9c59363e7dd35cb7c19d8736b102d99/tenor.gif?itemid=13730968',
	'https://media1.tenor.com/images/d3386f6caeea27736f95166eb52ebb12/tenor.gif?itemid=14184806',
	'https://media.tenor.com/images/6b7f36a01c09766e366e9a6d35a7d744/tenor.gif',
	'https://media.tenor.com/images/5d3019942602cc8b7a548dd523947826/tenor.gif',
	'https://media.tenor.com/images/54aa95a2ed4ff6fd7cbc9317e6e102fb/tenor.gif',
	'https://media.tenor.com/images/ba4ea2dc5fbe3e8da294fbb27e40d76c/tenor.gif',
	'https://media1.tenor.com/images/d109931a1d23a6888582f71cf45fa2cf/tenor.gif?itemid=15124842',
	'https://media.tenor.com/images/05aa78167d8882a82c0fe4b6de82c179/tenor.gif',
	'https://media.tenor.com/images/d82e6b57ae2acd5d6b9c8833e07e398d/tenor.gif',
	]

	embed = discord.Embed(title=context.guild.name, description="( ಠ ͜ʖಠ) Oh yeah baby. . .", color=0x6A5ACD)
	embed.set_image(url=random.choice(milosList))
	await context.send(embed=embed)	