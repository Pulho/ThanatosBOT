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
from config.setup import bot

class Player:
    def __init__ (self, id):
        self.server_ID = id
        self.Is_playing = False
        self.song_Paused = False
        self.on_Voice_channel = False
        self.exceptOnJoin = False
        self.queue = [] 
    def playing(self):
        return self.Is_playing
    def paused(self):
        return self.song_Paused
    def on_Voice(self):
        return self.on_Voice_channel

Server = {} # Dictionary Vazio    
def checkServer(serverID):
	if Server.get(serverID) == None:
		Server[serverID] = Player(serverID)
	
@bot.command(pass_context=True)
async def consoleDebugger(context):
	for x,y in Server.items():
		print(x,y)

@bot.command(pass_context=True) # Done, Exception solved
async def join(context):
	checkServer(context.message.guild.id)
	thisServer = Server.get(context.message.guild.id)
	
	if thisServer.on_Voice_channel == False:
		try:
			channel = context.message.author.voice.channel
			await channel.connect()
			await context.send(f'Connected to voice channel: {channel}')
		except AttributeError:
			thisServer.exceptOnJoin = True
			await context.send(f'{context.message.author.mention} Not in a voice channel')

		if thisServer.exceptOnJoin == False:
			print(channel)
			print(f'{context.message.guild.id}: Channel {channel}')
			thisServer = Server.get(context.message.guild.id)
			thisServer.on_Voice_channel = True
			Server[context.message.guild.id] = thisServer
		else:
			thisServer.exceptOnJoin = False
			Server[context.message.guild.id] = thisServer
	else:
		print(f'{context.message.guild.id}: Already connect to a voice channel')
		await context.send('Im already on a voice channel')

@bot.command(pass_context=True)
async def leave(context):
	checkServer(context.message.guild.id)
	thisServer = Server.get(context.message.guild.id)

	if thisServer.on_Voice_channel == True:
		server = context.message.guild.voice_client
		await server.disconnect()
		thisServer.on_Voice_channel = False
	else:
		print(f'{context.message.guild.id}: Bot not in a voice channel')
		await context.send(f'I have to be in a voice channel first')

def check_Queue(context):
	thisServer = Server.get(context.message.guild.id)
	if thisServer.queue != []:
		video = thisServer.queue.pop(0)
		best_audio = video.getbestaudio()
'''
		embed = discord.Embed(title=video.title, description=f"Requested by {context.message.author.mention}", color=0x00ff00)
		embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/408656896497549312/b86889f66ec6983d26624e9c61a32f1e.png')
		embed.set_image(url=video.thumb)
		embed.add_field(name="Duration", value=video.duration, inline=False)
		embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)
		context.send(embed=embed)	
'''
		Server[context.message.guild.id] = thisServer
		server = context.message.guild.voice_client
		server.play(discord.FFmpegPCMAudio(best_audio.url), after=lambda: check_Queue(context))
'''
@bot.command(pass_context=True)
async def queue(context, url):
	server = context.message.guild.voice_client
'''
@bot.command(pass_context=True)
async def playerDebugger(context):
	thisServer = Server.get(context.message.guild.id)
	print(thisServer.queue)

@bot.command(pass_context=True)
async def play(context, url):
	video = pafy.new(url)

#	embed = discord.Embed(title=video.title, description=f"Requested by {context.message.author.mention}", color=0x00ff00)
#	embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/408656896497549312/b86889f66ec6983d26624e9c61a32f1e.png')
#	embed.set_image(url=video.thumb)
#	embed.add_field(name="Duration", value=video.duration, inline=False)
#	embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)
#	await context.send(embed=embed)	

	best_audio = video.getbestaudio()
	server = context.message.guild.voice_client
	thisServer = Server.get(context.message.guild.id)

	try:
		server.play(discord.FFmpegPCMAudio(best_audio.url), after=lambda e: check_Queue(context))
		embed = discord.Embed(title=video.title, description=f"Requested by {context.message.author.mention}", color=0x00ff00)
		embed.set_thumbnail(url='https://cdn.discordapp.com/app-icons/408656896497549312/b86889f66ec6983d26624e9c61a32f1e.png')
		embed.set_image(url=video.thumb)
		embed.add_field(name="Duration", value=video.duration, inline=False)
		
		embed.add_field(name="Try our premium freature to create playlists", value="Thanatos, killing your boredom", inline=False)
		await context.send(embed=embed)	

	except:
		thisServer.queue.append(video)
		Server[context.message.guild.id] = thisServer
'''
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

		server.play(discord.FFmpegPCMAudio(best_audio.url), after=lambda e: print('done', e))
		print(f'Server ID: {context.message.guild.id}')
		print(MusicPlayer.reproduction[context.message.guild.id])
'''