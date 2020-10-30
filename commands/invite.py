import discord
from config.setup  import bot

@bot.command() # Done
async def invite(context):
	embed = discord.Embed(title="Thanatos", description=f"Check your private messages for Invite link!", color=0x6A5ACD)
	embed.set_image(url="https://cdn.discordapp.com/app-icons/408656896497549312/b86889f66ec6983d26624e9c61a32f1e.png?size=512")
	embed.add_field(name="Note from the developer: ", value="Im still in development, now on Beta dont mind my bugs hehe. Thank you for supporting me!", inline=False)
	embed.add_field(name="Discord Link: ", value="https://discordapp.com/api/oauth2/authorize?client_id=408656896497549312&permissions=271838224&scope=bot", inline=False)
	await context.send(embed=embed)	