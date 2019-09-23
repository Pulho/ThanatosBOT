from config.setup  import bot

@bot.command(pass_context=True) # Done
async def invite(context):
	await context.send('Check your private messages for Invite link!')
	await context.author.send('Im still in development, dont mind my bugs hehe. Thank you for supporting me!\nhttps://discordapp.com/oauth2/authorize?client_id=408656896497549312&scope=bot')
