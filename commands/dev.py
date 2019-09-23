from config.setup  import bot

@bot.command(pass_context=True) # Done
async def dev(context):
	await context.send('Actual crew:\nDev: Paulo Victor (https://github.com/Pulho)')
	await context.send('Database manager: Paulo Vinicius (https://github.com/pvfls)')
	await context.send('Business/Visual art: João Alberto (https://github.com/joaoalbertos)')
