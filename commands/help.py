from config.setup  import bot

@bot.command(pass_context=True) # Done / Update
async def Help(context, command=None):
	if command != None:
		if command == 'dev':
			await context.send('See the production team of the Bot')
		elif command == 'ping':
			await context.send('Response time of the bot')
		elif command == 'play':
			await context.send('Play a specific URL')
		elif command == 'resume':
			await context.send('Resume a paused song')
		elif command == 'stop':
			await context.send('Stop reproduction song and reset the List')
		elif command == 'pause':
			await context.send('Pause the song')
		else:
			await context.send('Command not found in the database')
	else:
		await context.send(f'Hello {context.message.author.mention}! may i help you? List of all commands:\ndev - See the production team of the Bot\nping - Response time of the bot\nplay - Play a specific URL\nresume - Resume a paused song\npause - Pause a song\nstop -Stop reproduction song and reset the List')
