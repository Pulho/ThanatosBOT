import discord
from commands import *
from discord.ext import commands

@bot.command(pass_context=True)
async def Help(context, command=None):
	await context.send(f'Hello {context.message.author.mention}! may i help you?')

	if command != None:
		if command == 'dev':
			await context.send('See the developer of this bot')
		elif command == 'ping':
			await context.send('Response time of the bot')
		else:
			await context.send('Command not found in the database')
	else:
		await context.send('List of all commands:\ndev - See the developer of this bot\nping - Response time of the bot')
