import discord
import asyncio
import os
import pafy
import random
import ffmpy
import math
import ffmpeg
import youtube_dl
#Pesquisar musica do youtube
import urllib.request
import urllib.parse
import re

from commands import *
from discord import FFmpegPCMAudio
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord.utils import get
from config.setup import bot

class Player:
    def __init__ (self):
	    self.voiceChannel = False
	    self.channelName = None 
	    self.isPlaying = False
	    self.mediaPlayer = None

	    self.queue = []
	    self.copyQueue = []
	    self.actualSongIndex = -1
	    self.nextSongEvent = asyncio.Event()

	   	# Not implemented yet
	    self.volume = 1.0
	    self.repeat = False
Server = {}

def checkServer(context):
	if Server.get(context.guild.id) == None:
		Server[context.guild.id] = Player()

@bot.command() # Done, Exception solved
async def join(context):
	checkServer(context)
	
	try:
		channel = context.message.author.voice.channel
	except AttributeError:
		channel = None
		pass

	voice = get(bot.voice_clients, guild=context.guild)
	if Server[context.guild.id].voiceChannel:
		if Server[context.guild.id].channelName == context.author.voice.channel:
			print(f'{context.guild.id} (join): Already connected to a voice channel')
			await context.send(f'{context.author.mention} Already connected to the voice channel')
		else:
			print(f'{context.guild.id} (join): Moving to channel {context.author.voice.channel}')
			await context.send(f'Moving to channel {context.author.voice.channel}')
			Server[context.guild.id].channelName = context.author.voice.channel
			await context.voice_client.move_to(context.author.voice.channel)			
	else:
		if channel != None:
			print(f'{context.guild.id} (join): Connected at channel: {context.author.voice.channel}')
			await context.send(f'Connected to {context.author.voice.channel}')
			Server[context.guild.id].voiceChannel = True
			Server[context.guild.id].channelName = context.author.voice.channel
			await context.author.voice.channel.connect()
		else:
			print(f'{context.guild.id} (join): {context.author} not connected to any voice channel')
			await context.send(f'{context.author} not connected to any voice channel')		

@bot.command()
async def leave(context):
	checkServer(context)

	voice_client = context.message.guild.voice_client
	if Server[context.guild.id].voiceChannel == False:
		print(f"{context.guild.id}: Bot was told to leave the voice channel, but was not in one")
		await context.send("I'm not in a voice channel")
	else:
		print(f'{context.guild.id} (leave): Leaving channel')
		del Server[context.guild.id]
		await voice_client.disconnect()

@bot.command()
async def queue(context, actualPage=1):
	checkServer(context)

	if not Server[context.guild.id].copyQueue:
		await context.send("No songs in queue")
		return
	size = len(Server[context.guild.id].copyQueue)
	totalPages = math.ceil(size/10)
	startIndex = (actualPage-1)*10

	if startIndex + 10 >= len(Server[context.guild.id].copyQueue):
		limit = len(Server[context.guild.id].copyQueue)
	else:
		limit = startIndex + 10

	embed = discord.Embed(title=f"{context.guild.name} Mediaplayer", color=0x6A5ACD)
	valueString = ""
	for index in range(startIndex, limit):
		if index == Server[context.guild.id].actualSongIndex:
			valueString = valueString + "```css\n" + f"{index}) {Server[context.guild.id].copyQueue[index].title}```\n"
		else:
			valueString = valueString + f"```\n{index}) {Server[context.guild.id].copyQueue[index].title}```\n"
	embed.add_field(name="Queued songs", value=valueString)
	embed.set_footer(text = f"Page: {actualPage}/{totalPages}", icon_url = context.author.avatar_url)
	await context.send(embed=embed)	

async def showSong(context,video):
	embed = discord.Embed(title=video.title, description=f"Requested by {context.author.mention}", color=0x6A5ACD)
	embed.set_thumbnail(url=context.author.avatar_url)
	embed.set_image(url=video.thumb)
	embed.add_field(name="Duration", value=video.duration, inline=False)
	embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)
	await context.send(embed=embed)	

@bot.command()
async def stop(context):
	voice = get(bot.voice_clients, guild=context.guild)

	if voice and voice.is_playing():
		print(f"{context.guild.id} (stop): Player cleared")
		Server[context.guild.id].queue.clear()
		queue[context.guild.id].clear()
		Server[context.guild.id].actualSongIndex = -1
		voice.stop()
		context.message.guild.voice_client.disconnect()
		await context.send("Music stopped")
	else:
		print(f"{context.guild.id} (stop): Not playing")
		await context.send("No music playing to be stopped")

@bot.command()
async def pause(context):
	voice = get(bot.voice_clients, guild=context.guild)

	if voice and voice.is_playing():
		print(f"{context.guild.id} (pause): Music paused, type !resume to return")
		voice.pause()
		await context.send("Music paused, type !resume to return")
	else:
		print(f"{context.guild.id} (pause): No music playing to be paused")
		await context.send("No music playing to be paused")
'''
@bot.command()
async def repeat(context):
	checkServer(context)

	if not Server[context.guild.id].repeat:
		await context.send("Repeat activated")
		Server[context.guild.id].repeat = True
	else:
		await context.send("Repeat deactivated")
		Server[context.guild.id].repeat = False

@bot.command()
async def volume(context, volumeValue=None):
	checkServer(context)

	if not volumeValue:
		await context.send("Please insert a value for volume ( 0.0 to 1.0 )")
	else:
		Server[context.guild.id].volume = volumeValue
'''
@bot.command()
async def resume(context):
	voice = get(bot.voice_clients, guild=context.guild)

	if voice and voice.is_paused():
		print(f"{context.guild.id} (resume): Resuming song")
		voice.resume()
		await context.send(f"Resuming song")
	else:
		print(f"{context.guild.id} (resume): Music is not paused or not playing")
		await context.send("Music is not paused or not playing")

async def serverPlayer(context):
	if Server[context.guild.id].queue != []:
		video = Server[context.guild.id].queue.pop(0)
		Server[context.guild.id].actualSongIndex = Server[context.guild.id].actualSongIndex + 1
		embed = discord.Embed(title=video.title, description=f"Requested by {context.author.mention}", color=0x6A5ACD)
		embed.set_image(url=video.thumb)
		embed.add_field(name="URL", value=f"https://www.youtube.com/watch?v={video.videoid}", inline=False)
		embed.add_field(name="Duration", value=video.duration, inline=False)
		embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)
		await context.send(embed=embed)	
		best_audio = video.getbestaudio()
		Server[context.guild.id].mediaPlayer.play(discord.FFmpegPCMAudio(best_audio.url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), after=lambda e: Server[context.guild.id].nextSongEvent.set())
		await Server[context.guild.id].nextSongEvent.wait()
		Server[context.guild.id].nextSongEvent.clear()
		await serverPlayer(context)

def youtubePlaylistTreatment(url, context):
	ytbPlaylist = pafy.get_playlist(url)
	videosUrl = []

	for index in range(len(ytbPlaylist['items'])):
		video = pafy.new(f"www.youtube.com/watch?v={ytbPlaylist['items'][index]['pafy'].videoid}")
		Server[context.guild.id].queue.append(video)
		Server[context.guild.id].copyQueue.append(video)

	return

def demultiplexUrlType(url):
	if url.find('youtube.com/watch?v=') != -1:
		if url.find('&list=') != -1:
			return 0
		return 1
	else:
		return 2

@bot.command()
async def play(context, *inputReceive):
	checkServer(context)

	if not inputReceive:
		await context.send("Please type the url link or the name of it")
		return
	url = " ".join(inputReceive)

	## Join function
	try:
		channel = context.message.author.voice.channel
	except AttributeError:
		channel = None
		pass

	voice = get(bot.voice_clients, guild=context.guild)

	if channel != None:
		if Server[context.guild.id].voiceChannel:
			if Server[context.guild.id].channelName != context.author.voice.channel:
				print(f'{context.guild.id}: Moving to channel {context.author.voice.channel}')
				Server[context.guild.id].channelName = context.author.voice.channel
				await context.voice_client.move_to(context.author.voice.channel)			
		else:
			print(f'{context.guild.id}: Connected at channel: {context.author.voice.channel}')
			await context.send(f'**Connected to {context.author.voice.channel}**')
			Server[context.guild.id].voiceChannel = True
			Server[context.guild.id].channelName = context.author.voice.channel
			await context.author.voice.channel.connect()
		## End of join function

		typeUrl = demultiplexUrlType(url)
		if typeUrl == 0:
			videos = youtubePlaylistTreatment(url, context)
		elif typeUrl == 1:
			video = pafy.new(url)
			Server[context.guild.id].queue.append(video)
			Server[context.guild.id].copyQueue.append(video)
		elif typeUrl == 2:
			query_string = urllib.parse.urlencode({"search_query" : url})
			html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
			search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
			video = pafy.new("http://www.youtube.com/watch?v=" + search_results[0])
			Server[context.guild.id].queue.append(video)
			Server[context.guild.id].copyQueue.append(video)

		voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=context.guild)

		await context.message.delete()
		if not voice_client.is_playing():
			Server[context.guild.id].mediaPlayer = context.guild.voice_client	
			await serverPlayer(context)
		else:
			print(f"{context.guild.id} (play): {video.title} Queued, position {len(Server[context.guild.id].queue)}")
			await context.send(f"**{video.title} Queued, position {len(Server[context.guild.id].copyQueue)}**")
		return
	else:
		print(f'{context.guild.id} (play): {context.author} not connected to any voice channel')
		await context.send(f'{context.author} not connected to any voice channel')	