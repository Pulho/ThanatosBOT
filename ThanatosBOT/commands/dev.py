import discord
from config.setup  import bot

@bot.command() # Done
async def dev(context):
	embed = discord.Embed(title="Thanatos Crew", color=0x6A5ACD)
	embed.add_field(name="Developer:", value="Paulo Victor (Pulho - https://github.com/Pulho)", inline=True)
	embed.add_field(name="Database manager:", value="Paulo Vinicius (MAIniac - https://github.com/pvfls)", inline=True)
	embed.add_field(name="Business/Visual art:", value="João Alberto (Sydren - https://github.com/joaoalbertos)", inline=True)
	embed.set_footer(text = "Thanatos, killing your boredom", icon_url = "https://cdn.discordapp.com/avatars/408656896497549312/3bcbce16bb2ea16126e3a1d38a7b09bd.png?size=512")
	await context.send(embed=embed)