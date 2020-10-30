import discord
from discord.ext import commands

__prefix__ = '!'
__token__ = ${{ secrets.THANATOS_TOKEN }}

bot = commands.Bot(command_prefix = __prefix__)
bot.remove_command("help")