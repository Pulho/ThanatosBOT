import setup
from bot.py import bot

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

@bot.command(pass_context=True)
async def dev(context):
	await context.send('Actual developer: Pulho (https://github.com/Pulho)')

@bot.command(pass_context=True)
async def ping(context):
	await context.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.command(pass_context=True)
async def join(context):
	channel = context.author.voice.voice_channel
	await bot.join_voice_channel(channel)