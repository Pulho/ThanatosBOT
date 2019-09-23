from config.setup  import bot

@bot.command(pass_context=True) # Done
async def ping(context):
	await context.send(f'Pong! {round(bot.latency * 1000)}ms')
