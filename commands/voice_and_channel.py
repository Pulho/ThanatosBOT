import discord
import asyncio
import os
import pafy
import random
import ffmpy
import math
import ffmpeg
import youtube_dl
from commands import *
from threading import Thread
from discord import FFmpegPCMAudio
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord.utils import get
from config.setup import bot

class Player:
    def __init__ (self, id):
	    self.id = id
	    self.voiceChannel = False
	    self.channelName = None 
	    self.isPlaying = False
	    self.ready = False

	    self.queue = []
	    self.index = 0

Server = {} # Dictionary Vazio  

def checkServer(context):
	if Server.get(context.guild.id) == None:
		Server[context.guild.id] = Player(context.guild.id)

@bot.command() # Done, Exception solved
async def join(context):
	checkServer(context)
	channel = context.message.author.voice.channel
	voice = get(bot.voice_clients, guild=context.guild)

	if Server[context.guild.id].voiceChannel:
		if Server[context.guild.id].channelName == context.author.voice.channel:
			print(f'{context.guild.id}: Already connected to a voice channel')
			await context.send(f'{context.author.mention} Already connected to the voice channel')
		else:
			print(f'{context.guild.id}: Moving to channel {context.author.voice.channel}')
			await context.send(f'Moving to channel {context.author.voice.channel}')
			Server[context.guild.id].channelName = context.author.voice.channel
			await context.voice_client.move_to(context.author.voice.channel)			
	else:
		print(f'{context.guild.id}: Connected at channel: {context.author.voice.channel}')
		await context.send(f'Connected to {context.author.voice.channel}')
		Server[context.guild.id].voiceChannel = True
		Server[context.guild.id].channelName = context.author.voice.channel
		await context.author.voice.channel.connect()

@bot.command()
async def leave(context):
	checkServer(context)

	voice_client = context.message.guild.voice_client
	if Server[context.guild.id].voiceChannel == False:
		print(f"{context.guild.id}: Bot was told to leave the voice channel, but was not in one")
		await context.send("I'm not in a voice channel")
	else:
		print(f'{context.guild.id} (leave): Canal {voice_client}')
		del Server[context.guild.id]
		await voice_client.disconnect()

def incrementIndex(context):
	print("Chegou Increment")
	Server[context.guild.id].index = Server[context.guild.id].index + 1
	return

def player(context, index):
	video = Server[context.guild.id].queue[index]

	print(f"{context.guild.id} (CheckQueue): Playing now {video.title}")
	best_audio = video.getbestaudio()
	server = context.guild.voice_client
	server.play(discord.FFmpegPCMAudio(best_audio.url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), after=lambda e: incrementIndex(context))
	return

async def online_Player(context, actualIndex):
	while Server[context.guild.id].index < len(Server[context.guild.id].queue):
		if actualIndex < Server[context.guild.id].index:
			print(f"actualIndex {actualIndex}\n\nIndex {Server[context.guild.id].index}")
			actualIndex = Server[context.guild.id].index

			try:
				video = Server[context.guild.id].queue[actualIndex]
			except IndexError:
				pass

			embed = discord.Embed(title=video.title, description=f"Requested by {context.author.mention}", color=0x6A5ACD)
			embed.set_thumbnail(url=context.author.avatar_url)
			embed.set_image(url=video.thumb)
			embed.add_field(name="Duration", value=video.duration, inline=False)
			embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)
			await context.send(embed=embed)	

			#Thread(target=player, args=(context,actualIndex)).start()
			loop = asyncio.get_event_loop()
			loop.run_in_executor(None, player, context, actualIndex)
	return
'''
async def showSong(context, actualIndex):
	while Server[context.guild.id].index < len(Server[context.guild.id].queue):
		if actualIndex < Server[context.guild.id].index:
			actualIndex = Server[context.guild.id].index

			video = Server[context.guild.id].queue[actualIndex]

			embed = discord.Embed(title=video.title, description=f"Requested by {context.author.mention}", color=0x6A5ACD)
			embed.set_thumbnail(url=context.author.avatar_url)
			embed.set_image(url=video.thumb)
			embed.add_field(name="Duration", value=video.duration, inline=False)
			embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)
			await context.send(embed=embed)	
	return
def check_Queue(context, index):
	if Server[context.guild.id].index < len(Server[context.guild.id].queue):
		Server[context.guild.id].index = index
		video = Server[context.guild.id].queue[index]

		print(f"{context.guild.id} (CheckQueue): Playing now {video.title}")
		best_audio = video.getbestaudio()
		server = context.guild.voice_client
		server.play(discord.FFmpegPCMAudio(best_audio.url, before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"), after=lambda: check_Queue(context,index+1))
	else:
		return

async def queue(context, selectPage=1):
	pages = ceil(Server[context.guild.id].index / 10)

	if selectPage > pages:
		return await context.send("Not available page")

	embed = discord.Embed(title="Queue " + str(selectPage) + "/" + str(pages), color=0x6A5ACD)
	for index in range((selectPage * 10)-1, 10):
		embed.add_field(name="Duration", value=video.duration, inline=False)
		embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)

	await context.send(embed=embed)	

'''
@bot.command()
async def play(context, url=None):
	checkServer(context)

	video = pafy.new(url)
	voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=context.guild)
	Server[context.guild.id].queue.append(video)

	if not voice_client.is_playing():
		songTask = asyncio.create_task(online_Player(context, -1))
		await songTask
	else:
		print(f"{video.title} Queued, position {len(Server[context.guild.id].queue)}")
		await context.send(f"{context.guild.id}: {video.title} Queued, position {len(Server[context.guild.id].queue)}")
	return