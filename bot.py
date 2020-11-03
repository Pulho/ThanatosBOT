from config.setup  import __token__, __prefix__, bot
from commands import ping, dev, gif, w2g, help, invite, voice_and_channel
from event import on_ready, on_member_join, on_member_remove

bot.run(__token__)