import discord
from config.setup  import bot

@bot.command() # Done / Update
async def help(context, command=None):
	embed = discord.Embed(title="Thanatos Guide", description=f"Requested by {context.author.mention}", color=0x6A5ACD)
	if command != None:
		if command == 'dev':
			await context.send('See the production team of the Bot')
		elif command == 'ping':
			await context.send('Response time of the bot')
		elif command == 'dog':
			await context.send('Random gif of some cute dog')
		elif command == 'cat':
			await context.send('Random gif of some cute cat')
		elif command == 'oursecret':
			await context.send('Hehe... i think its better you find by yourself...')
		elif command == 'invite':
			await context.send('Generate a link to invite me for your server')
		elif command == 'play':
			await context.send('Play a specific URL or search the name on youtube')
		elif command == 'resume':
			await context.send('Resume a paused song')
		elif command == 'stop':
			await context.send('Stop reproduction song and clear the queue')
		elif command == 'pause':
			await context.send('Pause the song')
		else:
			await context.send('Command not found in the database')
			return
	else:
		generalFunctions = "```asciidoc\nGeneral Functions\ndev       :: See the production team of the Bot\nping      :: Response time of the bot\ndog       :: Random gif of some cute dog\ncat       :: Random gif of some cute cat\noursecret :: Some Milos gifs\ninvite    :: Link to invite me for your server\n\n\n"
		voiceFunctions   = "Voice Functions\njoin      :: Join voice channel\nleave     :: Leave actual voice channel\nplay <*>  :: Play the url or search on ytb and play\npause     :: Pause the song\nresume    :: Resume a paused song\nstop      :: Stop reproduction song and clear the queue\nskip      :: Skip to the next song\nskip to   :: Skip to the referred index\nqueue     :: Shows songs in queue list```"
		valueString = generalFunctions + voiceFunctions
		embed.add_field(name="List of all functions from Thanatos", value=valueString, inline=True)
		embed.set_footer(text = "Thanatos, killing your boredom", icon_url = "https://cdn.discordapp.com/avatars/408656896497549312/3bcbce16bb2ea16126e3a1d38a7b09bd.png?size=512")
		await context.send(embed=embed)