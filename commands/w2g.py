import requests
import re
import discord
from config.setup import bot, __w2g__token__

@bot.command() # Done / Update
async def w2g(context, URL=None):
	json = {
	    "w2g_api_key" : __w2g__token__,
	    "share" : URL,  # URL of the video to share - optional
	    "bg_color" : "#240a23", # Background color of the room in HTML notation - optional
	    "bg_opacity" : "80" # Background opacity of the room (0 - 100) - optional
	}
	url = 'https://w2g.tv/rooms/create.json'

	requestAnswer = requests.post(url, data = json)
	result = re.search('"streamkey":"(.*)"', requestAnswer.text)
	await context.send(f"**Your temporary Watch2Gether room!**\nhttps://w2g.tv/rooms/{result.group(1)[:18]} ( Expires after 1 day)")