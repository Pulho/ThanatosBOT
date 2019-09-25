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
        self.reproductionList = []
    def playing(self):
        return self.Is_playing
    def paused(self):
        return self.song_Paused
    def on_Voice(self):
        return self.on_Voice_channel

Server = {} # Dictionary Vazio    

def updateServer(ServerID):
	thisServer = Server.get(ServerID)
	print(f'Testing{thisServer.server_ID}')
	thisServer.on_Voice_channel = True
	return thisServer

def voice_Status(serverID):
	thisServer = Server.get(serverID)
	return thisServer.on_Voice_channel

@bot.command(pass_context=True)
async def consoleDebugger(context):
	for x,y in Server.items():
		print(x,y)

@bot.command(pass_context=True) # Done, Exception solved
async def join(context):
	if Server.get(context.message.guild.id) == None:
		Server[context.message.guild.id] = Player(context.message.guild.id)
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
	if Server.get(context.message.guild.id) == None:
		Server[context.message.guild.id] = Player(context.message.guild.id)
	
	thisServer = Server.get(context.message.guild.id)

	if thisServer.on_Voice_channel == True:
		server = context.message.guild.voice_client
		await server.disconnect()
		thisServer.on_Voice_channel = False
	else:
		print(f'{context.message.guild.id}: Bot not in a voice channel')
		await context.send(f'I have to be in a voice channel first')