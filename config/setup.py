import discord
from discord.ext import commands

__prefix__ = '!'
__token__ = ${{ secrets.THANATOS_TOKEN }}
 __w2g__token__ = ${{ secrets.W2G_TOKEN }}

bot = commands.Bot(command_prefix = __prefix__)
bot.remove_command("help")