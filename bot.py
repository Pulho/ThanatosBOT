import discord
import asyncio
import os
import pafy
import random
import ffmpy
from youtube_dl import YoutubeDL
from commands import *
from discord.voice_client import VoiceClient
from discord.ext import commands

__prefix__ = '!'
__token__ = 'NDA4NjU2ODk2NDk3NTQ5MzEy.DVTO7w.3SKVdlK6_1OLI8Jx0u7-UHIGpFY'

class MusicPlayer:
	Is_playing = False
	song_Paused = False
	on_Voice_channel = False
	reproductionList = {}
serverMusicPlayer = {}

@bot.event
async def on_ready():
	await bot.change_presence(activity=discord.Game(name='Type !Help for more'))
	print('Bot is Ready')

@bot.event
async def on_member_join(member):
	print(f'{member} has joined a server.')

@bot.event
async def on_member_remove(member):
	print(f'{member} has left a server.')

@bot.command(pass_context=True) # Done
async def ping(context):
	await context.send(f'Pong! {round(bot.latency * 1000)}ms')

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

@bot.command(pass_context=True) # Done
async def dev(context):
	await context.send('Actual crew:\nDev: Paulo Victor (https://github.com/Pulho)')
	await context.send('Database manager: Paulo Vinicius (https://github.com/pvfls)')
	await context.send('Business/Visual art: João Alberto (https://github.com/joaoalbertos)')

@bot.command(pass_context=True) # Done
async def invite(context):
	await context.send('Check your private messages for Invite link!')
	await context.author.send('Im still in development, dont mind my bugs hehe. Thank you for supporting me!\nhttps://discordapp.com/oauth2/authorize?client_id=408656896497549312&scope=bot')

@bot.command(pass_context=True) # Done, Exception solved
async def join(context):
	try:
		channel = context.message.author.voice.channel
		print(f'Channel {channel}')
		await channel.connect()
		await context.send(f'Connected voice channel: {channel}')
		MusicPlayer.on_Voice_channel = True
	except:
		print('Already connect to a voice channel')
		await context.send('Im already on a voice channel')
		pass
	print(f'Voice state = {MusicPlayer.on_Voice_channel}')

@bot.command(pass_context=True) # Done, Exception Okay
async def leave(context):
	if MusicPlayer.on_Voice_channel == True:
		server = context.message.guild.voice_client
		await server.disconnect()
		MusicPlayer.on_Voice_channel = False
	else:
		print(f'Im not in a voice channel')
		await context.send(f'I have to be in a voice channel first!')
	print(f'Voice state = {MusicPlayer.on_Voice_channel}')


@bot.command(pass_context=True)
async def play(context, url):
	if(serverMusicPlayer[context.message.guild.id].on_Voice_channel)
		print('Already connect to a voice channel')
	else
		try
			channel = context.message.author.voice.channel
			await channel.connect()
		except:
			print('Already connect to a voice channel')
			pass
	
	if serverMusicPlayer[context.message.guild.id].is_playing() == True:
		serverMusicPlayer[context.message.guild.id].reproductionList.append(url)
		return
	else
		video = pafy.new(url)

		embed = discord.Embed(title=video.title, description=f"Requested by {context.message.author.mention}", color=0x00ff00)
		embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/408656896497549312/b86889f66ec6983d26624e9c61a32f1e.png')
		embed.set_image(url=video.thumb)
		embed.add_field(name="Duration", value=video.duration, inline=False)
		embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)
		await context.send(embed=embed)	

		best_audio = video.getbestaudio()
		server = context.message.guild.voice_client

		MusicPlayer.reproductionList[context.message.guild.id] = video
		MusicPlayer.audioPlayer[context.message.guild.id] = server
		server.play(discord.FFmpegPCMAudio(best_audio.url), after=lambda e: print('done', e))
		print(f'Server ID: {context.message.guild.id}')
		print(MusicPlayer.reproduction[context.message.guild.id])

@bot.command(pass_context=True)
async def cat(context):
	catList =[
		'https://giphy.com/gifs/funny-cat-mlvseq9yvZhba',
		'https://giphy.com/gifs/JIX9t2j0ZTN9S',
		'https://giphy.com/gifs/leroypatterson-cat-glasses-CjmvTCZf2U3p09Cn0h',
		'https://giphy.com/gifs/cat-funny-WXB88TeARFVvi',
		'https://giphy.com/gifs/tiktok-aww-hTgmFytUwwHLaMahU1',
		'https://giphy.com/gifs/cat-bye-er19eYafoFxrq',
		'https://giphy.com/gifs/C9x8gX02SnMIoAClXa',
		'https://giphy.com/gifs/reaction-Nm8ZPAGOwZUQM',
		'https://giphy.com/gifs/cat-kisses-hugs-MDJ9IbxxvDUQM',
		'https://giphy.com/gifs/animals-being-jerks-xtGpIp4ixR6Gk',
		'https://giphy.com/gifs/aww-11s7Ke7jcNxCHS',
		'https://giphy.com/gifs/transparent-baby-shake-nNxT5qXR02FOM',
		'https://giphy.com/gifs/cat-moment-remember-8vQSQ3cNXuDGo',
		'https://giphy.com/gifs/cat-humour-funny-ICOgUNjpvO0PC',
		'https://giphy.com/gifs/cat-weird-bra-p4xp4BjHIdane',
		'https://giphy.com/gifs/banggood-cat-pets-dacing-xJjs8eGVbjNYY',
		'https://giphy.com/gifs/kitty-smart-1iu8uG2cjYFZS6wTxv',
		'https://giphy.com/gifs/funny-efHwZH4DeN9ss',
		'https://giphy.com/gifs/cheezburger-cat-mountain-good-job-fXgKfzV4aaHQI',
		'https://giphy.com/gifs/cat-adorable-cuddle-PibhPmQYXZ7HO',
		'https://giphy.com/gifs/weinventyou-3rgXBN6i9LIUg6lSLe',
		'https://giphy.com/gifs/ign-describe-plans-13HBDT4QSTpveU',
		'https://giphy.com/gifs/tT0wtdSJvE0Rq',
		'https://giphy.com/gifs/Lp5wuqMOmLUaAd0jBG',
		'https://giphy.com/gifs/cat-lasers-cucumber-3oEduQAsYcJKQH2XsI',
		'https://giphy.com/gifs/cat-i-cant-mo8MAe2maHrva',
		'https://giphy.com/gifs/cheezburger-cat-kittens-dj-t7MWRoExDRF72',
		'https://giphy.com/gifs/cat-box-legs-10SAlsUFbyl5Dy',
		'https://giphy.com/gifs/8cErt0PCSgzOY375br',
		'https://giphy.com/gifs/cat-fail-fat-lN9amhr8GZMhG',
		'https://giphy.com/gifs/cat-kitten-kids-Q56ZI04r6CakM',
		'https://giphy.com/gifs/funny-cat-gato-gatos-tBxyh2hbwMiqc',
		'https://giphy.com/gifs/cat-walking-table-vlUCWLGF7jpwA',
		'https://giphy.com/gifs/Zdfwny4fjIu2s',
		'https://giphy.com/gifs/cat-cute-trippy-26xBEez1vnVb2WgBq',
		'https://giphy.com/gifs/cat-spinning-roomba-qoxM1gi6i0V9e',
		'https://giphy.com/gifs/9VgB7x6yTpvOMHauzh',
		'https://giphy.com/gifs/v6aOjy0Qo1fIA',
		'https://giphy.com/gifs/cute-aww-eyebleach-LYd7VuYqXokv20CaEG',
		'https://giphy.com/gifs/reaction-mood-3dpGaQxDQthaQDeWFF',
		'https://giphy.com/gifs/cat-fluffy-XMxPoXBNpjrRC',
		'https://giphy.com/gifs/cat-disney-sad-pncpd012ij3qw',
		'https://giphy.com/gifs/82CItLnbSh8hzsXK3H',
		'https://giphy.com/gifs/loop-cat-EmMWgjxt6HqXC',
		'https://giphy.com/gifs/1PgFpz0u4diQRuHyvE',
		'https://giphy.com/gifs/23eIaihzejUmUtIDkO',
		'https://giphy.com/gifs/cat-loop-exercise-hpJOl7t4qeh5m',
		'https://giphy.com/gifs/cat-cute-roomba-3iBcRAErFhFwoTVbN5',
		'https://giphy.com/gifs/b5XJRNBrvgVHjkTsRV',
		'https://giphy.com/gifs/cat-fat-crunches-KgcjJH2LgCmMo',
		'https://giphy.com/gifs/viralhog-funny-cat-cute-4QFzZTjadMFPynIRea',
		'https://giphy.com/gifs/cat-cute-box-hGLdrItUOxou4',
		'https://giphy.com/gifs/d3zUEBN9RdNE4',
		'https://giphy.com/gifs/cat-turtle-eY2Q6hxp1ZeFi',
		'https://giphy.com/gifs/tkM2AQZpPCDhC',
		'https://giphy.com/gifs/cat-back-pig-6ureN5mMrHAxq',
		'https://giphy.com/gifs/cat-skateboard-fSbYwraWQuCKQ',
		'https://giphy.com/gifs/cat-maru-loop-Mhy9hKgfwI0lG'
	]

	await context.send(random.choice(catList))

@bot.command(pass_context=True)
async def dog(context):
	dogList = [
		'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9',
		'https://giphy.com/gifs/frustration-ANWIS2HYfROI8',
		'https://giphy.com/gifs/fpXxIjftmkk9y',
		'https://giphy.com/gifs/morning-perfect-loops-bbshzgyFQDqPHXBo4c',
		'https://giphy.com/gifs/RQSuZfuylVNAY',
		'https://giphy.com/gifs/reaction-dog-omg-21GCae4djDWtP5soiY',
		'https://giphy.com/gifs/lap-QvBoMEcQ7DQXK',
		'https://giphy.com/gifs/cute-aww-eyebleach-fnlXXGImVWB0RYWWQj',
		'https://giphy.com/gifs/dog-blah-srb6bXZHbgDsc',
		'https://giphy.com/gifs/3lxD1O74siiz5FvrJs',
		'https://giphy.com/gifs/dog-eyebleach-im-flying-Y4pAQv58ETJgRwoLxj',
		'https://giphy.com/gifs/dude-VkIet63SWUJa0',
		'https://giphy.com/gifs/EExhQTbQ75Hxq3KcOp',
		'https://giphy.com/gifs/3o7TKSha51ATTx9KzC',
		'https://giphy.com/gifs/k2Da0Uzaxo9xe',
		'https://giphy.com/gifs/dog-hungry-animal-cruelty-1rPVq3R9acPilzfLZO',
		'https://giphy.com/gifs/reaction-DZR39sOOQWP8A7UoVs',
		'https://giphy.com/gifs/1d7F9xyq6j7C1ojbC5',
		'https://giphy.com/gifs/mrw-bathroom-nekkid-DvyLQztQwmyAM',
		'https://giphy.com/gifs/wjK3YnjoQf0go',
		'https://giphy.com/gifs/stupid-cabbage-WLbtNNR5TKJBS',
		'https://giphy.com/gifs/reaction-mood-gGeyr3WepujbGn7khx',
		'https://giphy.com/gifs/cheezburger-dog-cage-fluff-26FPqut4lzK3AECEo',
		'https://giphy.com/gifs/swimming-pug-dog-r6ALgGVKLg93O',
		'https://giphy.com/gifs/Bc3SkXz1M9mjS',
		'https://giphy.com/gifs/corgi-HUfTNG6lOZNK',
		'https://giphy.com/gifs/afv-funny-fail-lol-3ornjU8Cd8FW1nhG6s',
		'https://giphy.com/gifs/dog-eyebrows-flbElEhvXDf7W',
		'https://giphy.com/gifs/reaction-mood-2YbW1T9e3gHcNbPq56',
		'https://giphy.com/gifs/dog-school-homework-3oEduXKKfBX6PPLiGQ',
		'https://giphy.com/gifs/ride-naXyAp2VYMR4k',
		'https://giphy.com/gifs/barkpost-dog-pizza-gif-3oz8xvhl6mTmF4MJI4',
		'https://giphy.com/gifs/lastweektonight-hbo-john-oliver-last-week-tonight-yoJC2COHSxjIqadyZW',
		'https://giphy.com/gifs/combined-gifs-4H5nOUqX7FywOGpCF7',
		'https://giphy.com/gifs/clever-disguise-BdhtvnPILhdYs',
		'https://giphy.com/gifs/HqzWVmrPy4B0c',
		'https://giphy.com/gifs/funny-cute-dog-bhSi84uFsp66s',
		'https://giphy.com/gifs/funny-dog-T7nRl5WHw7Yru',
		'https://giphy.com/gifs/dog-butterfly-10AVDflAKRV86A',
		'https://giphy.com/gifs/lol-BpDYodBlBXFIs',
		'https://giphy.com/gifs/shoes-kGABMRdGVWKgE',
		'https://giphy.com/gifs/version-shadow-colossus-sE6jQonM5S8mI',
		'https://giphy.com/gifs/reaction-mood-4H1znPjeKmZXAIF4qw',
		'https://giphy.com/gifs/afv-funny-fail-lol-26tPjh5FzTLPI5wcw',
		'https://giphy.com/gifs/reaction-9xhPHhPLlRThasqXlH',
		'https://giphy.com/gifs/4HeScCadLcoNQkKdaJ',
		'https://giphy.com/gifs/shopping-zkcXND5kY4POU',
		'https://giphy.com/gifs/dog-roll-over-ZThQqlxY5BXMc',
		'https://giphy.com/gifs/dog-hello-pun-yoJC2qNujv3gJWP504',
		'https://giphy.com/gifs/FDHDP7DREKSlYtHm43',
		'https://giphy.com/gifs/dog-skillz-j7ieM4wLOaNu8',
		'https://giphy.com/gifs/dog-scared-car-Hw1FAuSamUk3m',
		'https://giphy.com/gifs/dog-spinner-fidget-yJHN2CCfPIw4o',
		'https://giphy.com/gifs/videos-end-looped-l4RJOXehZXoQM',
		'https://giphy.com/gifs/cheezburger-dog-bath-shampoo-AGeAjEThf5U2Y',
		'https://giphy.com/gifs/afv-funny-fail-lol-xTk9ZH5U5vb76JhNHa',
		'https://giphy.com/gifs/dog-puppy-pArhCgHcVcyRO'
	]

	await context.send(random.choice(dogList))

@bot.command(pass_context=True) # Done
async def pause(context):
	try:
		if MusicPlayer.song_Paused == False:
			server = context.message.guild.voice_client
			server.pause()
			await context.send(f'Song paused, type !resume for return the song {context.message.author.mention}')
			MusicPlayer.song_Paused = True
		else:
			await context.send(f'Song already paused! {context.message.author.mention}')
	except AttributeError:
		await context.send('Im not playing any music')

@bot.command(pass_context=True) # Done
async def resume(context):
	try:
		if MusicPlayer.song_Paused == True:
			server = context.message.guild.voice_client
			server.resume()
		else:
			await context.send(f'There is no song paused to resume {context.message.author.mention}')
	except AttributeError:
		await context.send('Im not playing any music')

@bot.command(pass_context=True) # Done
async def stop(context):
	try:
		server = MusicPlayer.audioPlayer[context.message.guild.id]
		server.stop()
		await server.disconnect()
	except AttributeError:
		pass

bot.run(__token__)