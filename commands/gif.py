import random
import discord
from config.setup  import bot
import urllib.parse
import urllib.request
import re

@bot.command()
async def gif(context, *inputReceive):
	if not inputReceive:
		await context.send("Please send the name of the gif you want to search")
		return
	search = "+".join(inputReceive)
	gifName = " ".join(inputReceive)

	html_content = urllib.request.urlopen("https://giphy.com/search/" + search)
	giphyList = re.findall(r'"url": "https://giphy.com/gifs/(.*?)"', html_content.read().decode())
	
	if not giphyList:
		await context.send(f"No results for {gifName}")
		return

	randomChoice = random.choice(giphyList)
	randomChoice = randomChoice.split("-")
	randomChoice = randomChoice[-1]
	url = "https://media0.giphy.com/media/"+ randomChoice + "/giphy.gif"
	embed = discord.Embed(title=f"{gifName}", color=0x6A5ACD)
	embed.set_footer(text = f"Access https://giphy.com for more", icon_url = "https://giphy.com/static/img/giphy_logo_square_social.png")
	embed.set_image(url=url)
	await context.send(embed=embed)	
