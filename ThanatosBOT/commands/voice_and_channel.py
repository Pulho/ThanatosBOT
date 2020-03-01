import discord
import asyncio
import os
import pafy
import random

#import ffmpy
import math
import ffmpeg

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

playlist = dict()

# Inicio parte do BD(pra executar o bot sem os comandos do BD é só comentar isso e 8 últimos comandos)
import MySQLdb
host = "localhost"
user = "VSCode"
password = "Fernandes12#"
db = "thanatos_music"
port = 3306

con = MySQLdb.connect(host, user, password, db, port)

c = con.cursor(MySQLdb.cursors.DictCursor)
#Fim da parte do BD

def select(fields, tables, where = None):
   
    global c
   
    query = "SELECT " + fields + " FROM " + tables

    if(where):
        query += " WHERE " + where
    
    c.execute(query)

    return c.fetchall()

def insert(values, table, fields=None):
    global c, con

    query = "INSERT INTO " + table

    if(fields):
        query += "( " + fields + ")" 

    query += " VALUES " + ",".join(["(" + v + ")" for v in values])

    print(query)
    c.execute(query)
    con.commit()

def update(sets, table, where=None):
    global c, con
    
    query = "UPDATE " + table
    
    query += " SET " + ",".join([field + " = '" + value + "'" for field, value in sets.items()])

    if(where):
        query+= " WHERE " + where
    
    c.execute(query)
    con.commit()

def deleteDB(table, where):

    global c, con

    query = "DELETE FROM " + table + " WHERE " + where
	
    c.execute(query)
    con.commit()

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
			valueString = valueString + "```css\n" + f"{index + 1}) {Server[context.guild.id].copyQueue[index].title}```\n"
		else:
			valueString = valueString + f"```\n{index + 1}) {Server[context.guild.id].copyQueue[index].title}```\n"
	embed.add_field(name="Queued songs", value=valueString)
	embed.set_footer(text = f"Page: {actualPage}/{totalPages}", icon_url = context.author.avatar_url)
	await context.send(embed=embed)	

@bot.command()
async def delete(context, index=None):
	checkServer(context)

	if not Server[context.guild.id].copyQueue:
		await context.send("Empty queue")
		return

	if index != None and index.isdigit():
		index = int(index) - 1
		if (index == None) or (index < 0 or index > len(Server[context.guild.id].copyQueue)):
			await context.send("Not a valid index")
			return

		if index == Server[context.guild.id].actualSongIndex:
			await context.send("Cannot delete the actual playing song")
			return

		if index < Server[context.guild.id].actualSongIndex:
			songRemoved = Server[context.guild.id].copyQueue.pop(index)
			Server[context.guild.id].actualSongIndex = Server[context.guild.id].actualSongIndex - 1
			await context.send(f"{songRemoved.title} removed from the queue")
		else:
			songRemoved = Server[context.guild.id].copyQueue.pop(index)
			print(f"Server Queue {Server[context.guild.id].queue}")
			print(f"Server actualSongIndex {Server[context.guild.id].actualSongIndex}")
			Server[context.guild.id].queue.pop((index - Server[context.guild.id].actualSongIndex - 1))
			await context.send(f"{songRemoved.title} removed from the queue")
	else:
		await context.send("Not a valid argument")
	return

@bot.command()
async def stop(context):
	checkServer(context)

	voice_client = context.message.guild.voice_client
	if Server[context.guild.id].mediaPlayer.is_playing():
		print(f"{context.guild.id} (stop): Player cleared")
		Server[context.guild.id].mediaPlayer.stop()
		Server[context.guild.id].queue.clear()
		Server[context.guild.id].actualSongIndex = -1
		await voice_client.disconnect()
		Server[context.guild.id].isPlaying = False
		Server[context.guild.id].queue = Server[context.guild.id].copyQueue.copy()
	else:
		print(f"{context.guild.id} (stop): Not playing")
		await context.send("No music playing to be stopped")

@bot.command()
async def pause(context):
	checkServer(context)

	if Server[context.guild.id].mediaPlayer.is_playing():
		print(f"{context.guild.id} (pause): Music paused, type !resume to return")
		Server[context.guild.id].mediaPlayer.pause()
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
	checkServer(context)

	if Server[context.guild.id].mediaPlayer.is_paused():
		print(f"{context.guild.id} (resume): Resuming song")
		Server[context.guild.id].mediaPlayer.resume()
		await context.send(f"Resuming song")
	else:
		print(f"{context.guild.id} (resume): Music is not paused or not playing")
		await context.send("Music is not paused or not playing")

@bot.command()
async def skip(context, *inputReceive):
	checkServer(context)

	if not inputReceive:
		if Server[context.guild.id].mediaPlayer.is_playing():
			if Server[context.guild.id].actualSongIndex + 1 < len(Server[context.guild.id].copyQueue):
				print(f"{context.guild.id} (skip): Skipping song")
				await context.send("Skipping")
				Server[context.guild.id].mediaPlayer.stop()
			else:
				await context.send("There's no next song yet")
	elif inputReceive[0] == "to":
		index = int(inputReceive[1]) - 1

		if Server[context.guild.id].mediaPlayer.is_playing():
			if index < len(Server[context.guild.id].copyQueue) and index > 0:
				print(f"{context.guild.id} (skip to {index}): Skipping song")
				Server[context.guild.id].queue = Server[context.guild.id].copyQueue[index:].copy()
				Server[context.guild.id].actualSongIndex = index
				await context.send(f"Skipping to {index + 1}")
				Server[context.guild.id].mediaPlayer.stop()
			else:
				await context.send("Not possible to skip to that index")
	return

@bot.command()
async def previous(context):
	checkServer(context)

	if Server[context.guild.id].mediaPlayer.is_playing():
		if Server[context.guild.id].actualSongIndex - 1 >= 0:
			index = Server[context.guild.id].actualSongIndex
			actualSong = Server[context.guild.id].copyQueue[index]
			prevSong   = Server[context.guild.id].copyQueue[index - 1]
			Server[context.guild.id].queue.insert(0, actualSong)
			Server[context.guild.id].queue.insert(0, prevSong)
			Server[context.guild.id].actualSongIndex = Server[context.guild.id].actualSongIndex - 2
			await context.send("Retrieving previous song")
			Server[context.guild.id].mediaPlayer.stop()
		else:
			await context.send("No possible to get the previous song")
	return

@bot.command()
async def repeat(context):
	checkServer(context)

	if Server[context.guild.id].mediaPlayer.is_playing():
		print("Entrou")
		if Server[context.guild.id].actualSongIndex < len(Server[context.guild.id].copyQueue):
			await context.send("Skipping")
			Server[context.guild.id].mediaPlayer.stop()
		else:
			await context.send("No possible to skip")
	return

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
		print("serverPlayer waiting lock")
		await Server[context.guild.id].nextSongEvent.wait()
		print("serverPlayer lock acquired")
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
	if url.find('youtube.com/') != -1:
		if url.find('watch?v=') != -1:
			return 0
		elif url.find('playlist?list='):
			return 1
	else:
		return 2

@bot.command()
async def play(context, *inputReceive):
	checkServer(context)

	if not inputReceive and Server[context.guild.id].queue == []:
		if not Server[context.guild.id].queue:
			await context.send("Please type the url link or the name of it")
		else:
			await serverPlayer(context)
		return
	url = " ".join(inputReceive)

	print(url)

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
			video = pafy.new(url)
			Server[context.guild.id].queue.append(video)
			Server[context.guild.id].copyQueue.append(video)
		elif typeUrl == 1: # Broken
			await context.send("This may take a while. . .")
			videos = youtubePlaylistTreatment(url, context)
		elif typeUrl == 2:
			await context.send(f"Searching for the best result for {url}. . .")
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
	else:
		print(f'{context.guild.id} (play): {context.author} not connected to any voice channel')
		await context.send(f'{context.author} not connected to any voice channel')	
	return

@bot.command()#Antiga mystuff
async def profile(context, *actualPage):

	auxQuery = "id_usuario = " + str(context.message.author.id)
	if not (select("*","usuarios",auxQuery)):
		await context.send("**You're not a Thanatos user yet, use !createp to create your first playist**")
		return

	auxStatus = "id_usuario = " + str(context.message.author.id)
	statusPremium = select("tipo","usuarios",auxStatus)

	auxQtd = "id_usuario = " + str(context.message.author.id)
	qtdPlaylists = select("qtd_playlists","usuarios",auxQtd)

	auxNomes = "fk_usuario = " + str(context.message.author.id)
	dadosPlaylist = select("nome,dur_total","playlists",auxNomes)

	userPremium = list(statusPremium[0].values())[0]
	quantityPlaylist = list(qtdPlaylists[0].values())[0]
	playlistName = []
	totalDuration = 0

	for i in range(quantityPlaylist):
		playlistName.append(list(dadosPlaylist[i].values())[0])
		totalDuration += list(dadosPlaylist[i].values())[1]

	title =f"**{context.author.name}'s Profile**\n"
	if userPremium == "FREE":
		prefix = "-"
		userPremium = False
	else:
		prefix = "+"
		userPremium = True


	information = f"**User Information**\n```diff\n{prefix} Premium status: {userPremium}\n+ Playlists number: {quantityPlaylist}\n+ Total duration: {totalDuration}sec```\n"

	if userPremium == False:
		prefix = "-"
		thplaylistPrefix = "+"
		if quantityPlaylist == 2:
			thplaylistPrefix = "-"
	elif userPremium:
		prefix = "+"
		thplaylistPrefix = "+"

	commands = f"**Commands**\n```diff\n{thplaylistPrefix} thplaylist <name>\n+ myshuffle <playlist name>\n+ myqueue <playlist name>\n{prefix} mycopy <User mention> <Playlist name>\n+ mydelete <index>\n+ myclear <playlist name>\n+ myrename <playlist oldname> <playlist newname>\n{prefix} myimportSpotify <URL Spotify playlist>```\n"
	
	playlists = f"**Playlists**\n```md\n"
	if quantityPlaylist > 0: 
		if not actualPage:
			actualPage = 1
		else:
			actualPage = int(actualPage[0])

		size = len(playlistName)
		totalPages = math.ceil(size/5)
		startIndex = (actualPage-1)*5

		if startIndex + 5 >= len(playlistName):
			limit = len(playlistName)
		else:
			limit = startIndex + 5
		for index in range(startIndex, limit):
			aux = len(str(playlistName[index])) - 1 
			playlists = playlists + f"# {index + 1}) {str(playlistName[index])[2:aux]}\n"

		playlists = playlists + "\n\nPage " + str(actualPage) + "/" + str(totalPages) + "```"
	else:
		playlists = playlists + "# 0) <Empty>\n\nIt seems that you don't have any playlist yet\ndon't worry, create one right now with\n!thplaylist <name>\nPage 1/1\n\n```"

	userProfile = title + information + commands + playlists
	await context.send(userProfile)

@bot.command()
async def createp(context, *inputReceive):
	checkServer(context)

	queryAux = "id_usuario = " + str(context.message.author.id)
	if select("*","usuarios",queryAux):
		pass
	else:
		usr = str(context.message.author.id) + ", DEFAULT, DEFAULT"
		values = [usr]
		insert(values, "usuarios")
	
		
	if not inputReceive and Server[context.guild.id].queue == []:
		if not Server[context.guild.id].queue:
			await context.send("Please type a name for your playlist!")
		else:
			await serverPlayer(context)
		return
	userCmd = " ".join(inputReceive)

	queryAux = "fk_usuario = " + str(context.message.author.id)
	queryAux2 = "id_usuario = " + str(context.message.author.id)

	queryAux = select("count(*)","playlists",queryAux)
	queryAux2 = select("id_usuario","usuarios",queryAux2)

	aux = list(queryAux[0].values())
	aux2 = list(queryAux2[0].values())
	
	auxQuery = "fk_usuario = " + str(context.message.author.id) + " and nome = " + "'" + userCmd + "'"

	if (str(aux[0]) == str(2)) and (str(aux2[0]) == str(context.message.author.id)):
		await context.send("As a free user you can only have 2 playlists at a time, adquire Thanatos Premium(http://siteFicticioQueJoaoDoentaoVaiFazer.com) for more!")
	elif select("*","playlists",auxQuery):
		await context.send(f'{userCmd} Already exist, use !setp <name> to manipulate it!')
	else: 
		cmd = str(context.message.author.id) + ", DEFAULT, " + "'" + userCmd + "'" + ", DEFAULT, DEFAULT"
		values = [cmd]
		insert(values, "playlists")
		await context.send(f'**{userCmd} was created!**')
	return

@bot.command()
async def listp(context, *inputReceive):

    auxQuery = "id_usuario = " + str(context.message.author.id)

    if not (select("*","usuarios",auxQuery)):
        await context.send("**You're not a Thanatos user yet, use !createp to create your first playlist**")
        return
	
    auxQuery = "fk_usuario = " + str(context.message.author.id)
    playlistList = list(select("nome,dur_total","playlists",auxQuery))

    auxQtd = "id_usuario = " + str(context.message.author.id)
    qtdPlaylists = select("qtd_playlists","usuarios",auxQtd)

    playlistQuantity = list(qtdPlaylists[0].values())[0]
	
    for i in range(playlistQuantity):
	    playlistList.append(playlistList[i].values())

    actualPage = 1

    musicOut = f"**Playlists from: {context.message.author}\n**```md\n"
    if playlistQuantity > 0: 

	    size = playlistQuantity
	    totalPages = math.ceil(size/15)
	    startIndex = (actualPage-1)*15

	    if startIndex + 15 >= playlistQuantity:
		    limit = playlistQuantity
	    else:
		    limit = startIndex + 15
	    for index in range(startIndex, limit):
		    aux = len(str(list(playlistList[index].values())[0]))
		    musicOut = musicOut + f"# {index + 1}) {str(list(playlistList[index].values()))[3:aux]}\t\t Duration:{list(playlistList[index].values())[1]}secs \n"

	    musicOut = musicOut + "\n\nPage " + str(actualPage) + "/" + str(totalPages) + "```"
    else:
	    musicOut = musicOut + "# 0) <Empty>\n\nIt seems that you don't have any musics yet\ndon't worry, add one right now with\n!setp <name> + !add <name>\nPage 1/1\n\n```"

    await context.send(musicOut)
	
@bot.command()#Antiga showp
async def setp(context, *inputReceive):

	auxQuery = "id_usuario = " + str(context.message.author.id)
	if not (select("*","usuarios",auxQuery)):
		await context.send("**You're not a Thanatos user yet, use !createp to create your first playlist**")
		return
	elif not inputReceive:
		await context.send("**Type the name of a existing playlist to manipulate!**")
		return
	userCmd = " ".join(inputReceive)

	#Begin Antiga setp
	global playlist

	print(f'User: {context.message.author.id}')

	auxQuery2 = "fk_usuario = " + str(context.message.author.id) + " and " + "nome = " + "'" + userCmd + "'"
	
	if(select("*","playlists",auxQuery2)):
		playlist[context.message.author.id] = userCmd
		await context.send(f'**You are into your {userCmd} playlist now, use !add to add a song or !deletem to delete it!\n\n  I will show you all songs, but this may take a while**')
	else:
		await context.send("There's no such playlist, use !createp to create it")
		return
	#End antiga setp
	
	auxQtd = "fk_usuario = " + str(context.message.author.id) + " and " + "nome = " + "'" + userCmd + "'"
	qtdMusicas = select("qtd_musicas","playlists",auxQtd)

	musicQuantity = list(qtdMusicas[0].values())[0]

	auxQuery = "fk_usuario = " + "'" + str(context.message.author.id) + "'" + " and " + "nome = " + "'" + userCmd  + "'"
	query = select("nome,dur_total","playlists",auxQuery)

	playlistName = list(query[0].values())[0]
	playlistDuration = list(query[0].values())[1]

	aux = "fk_usuario = " + str(context.message.author.id) + " and " + "nome = " + "'" + userCmd + "'"
	auxQuery = list(select("id_playlist","playlists",aux)[0].values())[0]

	
	auxQuery2 = "fk_usuario = " + "'" + str(context.message.author.id) + "'" + " and " + "fk_playlist = " + "'" + str(auxQuery)  + "'"
	query2 = select("id_musica,ordem","musicas",auxQuery2)

	musics = []
	order = []
	
	for i in range(musicQuantity):
		musics.append(pafy.new(list(query2[i].values())[0]))
		order.append(list(query2[i].values())[1])
		print(musics[i].title,i)
		print(order[i], i)
		
	actualPage = 1

	aux = len(str(playlistName)) - 1
	musicOut = f"**PlaylistName: {str(playlistName)[2:aux]}\t\t Duration: {playlistDuration}sec\n**```md\n"
	if musicQuantity > 0: 

		size = musicQuantity
		totalPages = math.ceil(size/15)
		startIndex = (actualPage-1)*15

		if startIndex + 15 >= musicQuantity:
			limit = musicQuantity
		else:
			limit = startIndex + 15
		for index in range(startIndex, limit):
			musicOut = musicOut + f"# {order[index]}) {musics[index].title}\n"

		musicOut = musicOut + "\n\nPage " + str(actualPage) + "/" + str(totalPages) + "```"
	else:
		musicOut = musicOut + "# 0) <Empty>\n\nIt seems that you don't have any musics yet\ndon't worry, add one right now with\n!setp <name> + !add <name>\nPage 1/1\n\n```"

	await context.send(musicOut)

@bot.command()
async def add(context, *inputReceive):
	
	global playlist

	checkServer(context)

	auxQuery = "id_usuario = " + str(context.message.author.id)
	if not (select("*","usuarios",auxQuery)):
		await context.send("**You're not a Thanatos user yet, use !createp to create your first playlist**")
		return

	if not inputReceive and Server[context.guild.id].queue == []:
		if not Server[context.guild.id].queue:
			await context.send(f'Please type a song name or url to be added on {playlist}')
		else:
			await serverPlayer(context)
		return
	userCmd = " ".join(inputReceive)

	url = userCmd

	typeUrl = demultiplexUrlType(url)
	if typeUrl == 0:
		video = pafy.new(url)
	elif typeUrl == 1: # Broken
		await context.send("This may take a while. . .")
		videos = youtubePlaylistTreatment(url, context)
	elif typeUrl == 2:
		await context.send(f"Searching for the best result for {url}. . .")
		query_string = urllib.parse.urlencode({"search_query" : url})
		html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
		search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
		video = pafy.new("http://www.youtube.com/watch?v=" + search_results[0])
		print(f"{video.title} was added to {playlist}")
		await context.send(f"**{video.title} was added to {playlist[context.message.author.id]}**")

	queryAux = "fk_usuario = " + str(context.message.author.id) + " and " + "nome = " + "'" + playlist[context.message.author.id] + "'"
	queryAux2 = select("id_playlist","playlists",queryAux)

	playlistId = list(queryAux2[0].values())

	aux = list(select("count(*)","musicas")[0].values())

	cmd = str(context.message.author.id) + ", '" + str(playlistId[0]) + "', " + "'" + str(video.videoid) + "'" + ", " + "'" + str(video.length) + "'" + ", " + "'" + str(aux[0]+1) + "'"
	values = [cmd]
	insert(values, "musicas")

@bot.command()
async def deletep(context, *inputReceive):
    checkServer(context)

    auxQuery = "id_usuario = " + str(context.message.author.id)
    if not (select("*","usuarios",auxQuery)):
	    await context.send("**You're not a Thanatos user yet, use !createp to create your first playlist**")
	    return

    if not inputReceive and Server[context.guild.id].queue == []:
	    if not Server[context.guild.id].queue:
		    await context.send("Please type a playlist name to delete")
	    else:
		    await serverPlayer(context)
	    return
    userCmd = " ".join(inputReceive)

    auxQuery = "nome = " + "'" + userCmd + "'"
    query = list(select("id_playlist","playlists",auxQuery)[0].values())

    auxQuery2 = "fk_playlist = " + str(query[0])

    if not (select("*","playlists",auxQuery)):
	    await context.send("**There's no such playlist to be deleted**")
    else:
        deleteDB("musicas",auxQuery2)
        deleteDB("playlists",auxQuery)
        await context.send(f'**Your playlist {userCmd} was deleted**')
    return

@bot.command()
async def deletem(context, *inputReceive):

	auxQuery = "id_usuario = " + str(context.message.author.id)
	if not (select("*","usuarios",auxQuery)):
		await context.send("**You're not a Thanatos user yet, use !createp to create your first playlist**")
		return

	if not inputReceive and Server[context.guild.id].queue == []:
		if not Server[context.guild.id].queue:
			await context.send("Please type the id of the music you want to delete")
		else:
			await serverPlayer(context)
		return
	userCmd = " ".join(inputReceive)

	auxDelete = "ordem = " + userCmd

	if not select("*","musicas",auxDelete):
		await context.send("**There's no such music on any playlists**")
	else:
		deleteDB("musicas",auxDelete)
		await context.send("**Your song was deleted!!!**")

@bot.command()
async def playp(context, *inputReceive):
    checkServer(context)

    auxQuery = "id_usuario = " + str(context.message.author.id)
    if not (select("*","usuarios",auxQuery)):
	    await context.send("**You're not a Thanatos user yet, use !createp to create your first playlist**")
	    return

    if not inputReceive:
        await context.send("Please type the url link or the name of it")
        return
    playlistName = " ".join(inputReceive)

    auxQuery = "fk_usuario = " + str(context.message.author.id) + " and nome = " + "'" + playlistName + "'"

    if not (select("*","playlists",auxQuery)):
        await context.send("Please choose one of the existing playlists or type !createp to create one!")
	    
    if not Server[context.guild.id].voiceChannel:
        try:
            channel = context.message.author.voice.channel
        except AttributeError:
            channel = None
            pass

        voice = get(bot.voice_clients, guild=context.guild)
        if Server[context.guild.id].voiceChannel:
            if Server[context.guild.id].channelName == context.author.voice.channel:
                print(f'{context.guild.id} (playp): Already connected to a voice channel')
                await context.send(f'{context.author.mention} Already connected to the voice channel')
            else:
                print(f'{context.guild.id} (playp): Moving to channel {context.author.voice.channel}')
                await context.send(f'Moving to channel {context.author.voice.channel}')
                Server[context.guild.id].channelName = context.author.voice.channel
                await context.voice_client.move_to(context.author.voice.channel)            
        else:
            if channel != None:
                print(f'{context.guild.id} (playp): Connected at channel: {context.author.voice.channel}')
                await context.send(f'Connected to {context.author.voice.channel}')
                Server[context.guild.id].voiceChannel = True
                Server[context.guild.id].channelName = context.author.voice.channel
                await context.author.voice.channel.connect()
            else:
                print(f'{context.guild.id} (playp): {context.author} not connected to any voice channel')
                await context.send(f'{context.author} not connected to any voice channel')        


    auxQtd = "fk_usuario = " + str(context.message.author.id) + " and " + "nome = " + "'" + playlistName + "'"
    qtdMusicas = select("qtd_musicas","playlists",auxQtd)

    musicQuantity = list(qtdMusicas[0].values())[0]

    aux = "fk_usuario = " + str(context.message.author.id) + " and " + "nome = " + "'" + playlistName + "'"
    auxQuery = list(select("id_playlist","playlists",aux)[0].values())[0]

    auxQuery2 = "fk_usuario = " + "'" + str(context.message.author.id) + "'" + " and " + "fk_playlist = " + "'" + str(auxQuery)  + "'"
    query2 = select("id_musica,dur","musicas",auxQuery2)

    musics = []

    for i in range(musicQuantity):
        video = pafy.new(list(query2[i].values())[0])
        Server[context.guild.id].queue.append(video)
        Server[context.guild.id].copyQueue.append(video)
        musics.append(list(query2[i].values())[0])
	
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild=context.guild)

    await context.message.delete()
    if not voice_client.is_playing():
	    Server[context.guild.id].mediaPlayer = context.guild.voice_client
	    await serverPlayer(context)
    else:
	    print(f"{context.guild.id} (playp): Playlist {playlistName} Queued")
	    await context.send(f"**{playlistName} Queued**")
	

