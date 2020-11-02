import discord
from discord.ext import commands

__prefix__ = '!'
#__token__ = ${{ secrets.THANATOS_TOKEN }}
__token__  ='NDA4NjU2ODk2NDk3NTQ5MzEy.WnM9ZA.Vmvw98s6e1SYdHOFjjRY5SAS39c'

bot = commands.Bot(command_prefix = __prefix__)
bot.remove_command("help")