import discord
import asyncio
import os
import pafy
import random
import ffmpy
import ffmpeg
import youtube_dl
from commands import *
from discord import FFmpegPCMAudio
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord.utils import get
from config.setup import bot

class Player:
    def __init__ (self, id):
	    self.id = id
	    self.voiceChannel = False
	    self.isPlaying = False
	    
	    self.queue = []
	    self.index = 0


Server = {} # Dictionary Vazio  

def checkServer(context):
	if Server.get(context.guild.id) == None:
		Server[context.guild.id] = Player(context.guild.id)

async def joinVoice(context):
	channel = context.message.author.voice.channel
	voice = get(bot.voice_clients, guild=context.guild)

	if Server[context.guild.id].voiceChannel:
		print(f'{context.guild.id}: Already connected to a voice channel')
		await context.send(f'{context.author.mention} Already connected to a voice channel')
	else:
		print(f'{context.guild.id}: Connected at channel: {context.author.voice.channel}')
		Server[context.guild.id].voiceChannel = True
		await context.author.voice.channel.connect()

@bot.command() # Done, Exception solved
async def join(context):
	checkServer(context)

	channel = context.message.author.voice.channel
	voice = get(bot.voice_clients, guild=context.guild)

	if Server[context.guild.id].voiceChannel:
		print(f'{context.guild.id}: Already connected to a voice channel')
		await context.send(f'{context.author.mention} Already connected to a voice channel')
	else:
		print(f'{context.guild.id}: Connected at channel: {context.author.voice.channel}')
		Server[context.guild.id].voiceChannel = True
		await context.author.voice.channel.connect()

@bot.command()
async def leave(context):
	checkServer(context)

	voice_client = context.message.guild.voice_client
	if not voice:
		print(f"{context.guild.id}: Bot was told to leave the voice channel, but was not in one")
		await context.send("I'm not in a voice channel")
	else:
		print(f'{context.guild.id} (leave): Canal {voice_client}')
		del Server[context.guild.id]
		await voice_client.disconnect()

@bot.command()
async def queue(context):
	indexSum = 0

	if Server[context.guild.id].queue == []:
		return await context.send("Currently there is no song in queue")
	
	#embed = discord.Embed(title=context.guild.name, description=f"Requested by {context.message.author.mention}", color=0x00ff00)
	#for song in Server[context.guild.id].queue:
	#	await context

def showSong(context, video):
	embed = discord.Embed(title=video.title, description=f"Requested by {context.message.author.mention}", color=0x00ff00)
	embed.set_thumbnail(url=context.author.message.avatar_url)
	embed.set_image(url=video.thumb)
	embed.add_field(name="Duration", value=video.duration, inline=False)
	embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)
	context.send(embed=embed)
	return

def check_Queue(context):
	if Server[context.guild.id].queue != []:
		video = Server[context.guild.id].queue.pop(0)
		Server[context.guild.id].index = Server[context.guild.id].index + 1

		print(f"{context.guild.id} (CheckQueue): Playing now {video.title}")

		best_audio = video.getbestaudio()
		server = context.guild.voice_client
		server.play(discord.FFmpegPCMAudio(best_audio.url), after=lambda: check_Queue(context))
	else:
		discord.FFmpegPCMAudio.clear()

@bot.command()
async def play(context, url=None):
	checkServer(context)

	video = pafy.new(url)
	voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=context.guild)

	if voice_client.is_playing():
		Server[context.guild.id].queue.append(video)
	else:
		best_audio = video.getbestaudio()
		voice_client.play(discord.FFmpegPCMAudio(best_audio.url), after=lambda: check_Queue(context))
	
