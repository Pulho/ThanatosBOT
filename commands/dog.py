import random
import discord
from config.setup  import bot

@bot.command(pass_context=True)
async def dog(context):
	dogList = [
		'https://giphy.com/gifs/4Zo41lhzKt6iZ8xff9',
		'https://giphy.com/gifs/frustration-ANWIS2HYfROI8',
		'https://giphy.com/gifs/fpXxIjftmkk9y',
		'https://giphy.com/gifs/morning-perfect-loops-bbshzgyFQDqPHXBo4c',
		'https://giphy.com/gifs/RQSuZfuylVNAY',
		'https://giphy.com/gifs/reaction-dog-omg-21GCae4djDWtP5soiY',
		'https://giphy.com/gifs/lap-QvBoMEcQ7DQXK',
		'https://giphy.com/gifs/cute-aww-eyebleach-fnlXXGImVWB0RYWWQj',
		'https://giphy.com/gifs/dog-blah-srb6bXZHbgDsc',
		'https://giphy.com/gifs/3lxD1O74siiz5FvrJs',
		'https://giphy.com/gifs/dog-eyebleach-im-flying-Y4pAQv58ETJgRwoLxj',
		'https://giphy.com/gifs/dude-VkIet63SWUJa0',
		'https://giphy.com/gifs/EExhQTbQ75Hxq3KcOp',
		'https://giphy.com/gifs/3o7TKSha51ATTx9KzC',
		'https://giphy.com/gifs/k2Da0Uzaxo9xe',
		'https://giphy.com/gifs/dog-hungry-animal-cruelty-1rPVq3R9acPilzfLZO',
		'https://giphy.com/gifs/reaction-DZR39sOOQWP8A7UoVs',
		'https://giphy.com/gifs/1d7F9xyq6j7C1ojbC5',
		'https://giphy.com/gifs/mrw-bathroom-nekkid-DvyLQztQwmyAM',
		'https://giphy.com/gifs/wjK3YnjoQf0go',
		'https://giphy.com/gifs/stupid-cabbage-WLbtNNR5TKJBS',
		'https://giphy.com/gifs/reaction-mood-gGeyr3WepujbGn7khx',
		'https://giphy.com/gifs/cheezburger-dog-cage-fluff-26FPqut4lzK3AECEo',
		'https://giphy.com/gifs/swimming-pug-dog-r6ALgGVKLg93O',
		'https://giphy.com/gifs/Bc3SkXz1M9mjS',
		'https://giphy.com/gifs/corgi-HUfTNG6lOZNK',
		'https://giphy.com/gifs/afv-funny-fail-lol-3ornjU8Cd8FW1nhG6s',
		'https://giphy.com/gifs/dog-eyebrows-flbElEhvXDf7W',
		'https://giphy.com/gifs/reaction-mood-2YbW1T9e3gHcNbPq56',
		'https://giphy.com/gifs/dog-school-homework-3oEduXKKfBX6PPLiGQ',
		'https://giphy.com/gifs/ride-naXyAp2VYMR4k',
		'https://giphy.com/gifs/barkpost-dog-pizza-gif-3oz8xvhl6mTmF4MJI4',
		'https://giphy.com/gifs/lastweektonight-hbo-john-oliver-last-week-tonight-yoJC2COHSxjIqadyZW',
		'https://giphy.com/gifs/combined-gifs-4H5nOUqX7FywOGpCF7',
		'https://giphy.com/gifs/clever-disguise-BdhtvnPILhdYs',
		'https://giphy.com/gifs/HqzWVmrPy4B0c',
		'https://giphy.com/gifs/funny-cute-dog-bhSi84uFsp66s',
		'https://giphy.com/gifs/funny-dog-T7nRl5WHw7Yru',
		'https://giphy.com/gifs/dog-butterfly-10AVDflAKRV86A',
		'https://giphy.com/gifs/lol-BpDYodBlBXFIs',
		'https://giphy.com/gifs/shoes-kGABMRdGVWKgE',
		'https://giphy.com/gifs/version-shadow-colossus-sE6jQonM5S8mI',
		'https://giphy.com/gifs/reaction-mood-4H1znPjeKmZXAIF4qw',
		'https://giphy.com/gifs/afv-funny-fail-lol-26tPjh5FzTLPI5wcw',
		'https://giphy.com/gifs/reaction-9xhPHhPLlRThasqXlH',
		'https://giphy.com/gifs/4HeScCadLcoNQkKdaJ',
		'https://giphy.com/gifs/shopping-zkcXND5kY4POU',
		'https://giphy.com/gifs/dog-roll-over-ZThQqlxY5BXMc',
		'https://giphy.com/gifs/dog-hello-pun-yoJC2qNujv3gJWP504',
		'https://giphy.com/gifs/FDHDP7DREKSlYtHm43',
		'https://giphy.com/gifs/dog-skillz-j7ieM4wLOaNu8',
		'https://giphy.com/gifs/dog-scared-car-Hw1FAuSamUk3m',
		'https://giphy.com/gifs/dog-spinner-fidget-yJHN2CCfPIw4o',
		'https://giphy.com/gifs/videos-end-looped-l4RJOXehZXoQM',
		'https://giphy.com/gifs/cheezburger-dog-bath-shampoo-AGeAjEThf5U2Y',
		'https://giphy.com/gifs/afv-funny-fail-lol-xTk9ZH5U5vb76JhNHa',
		'https://giphy.com/gifs/dog-puppy-pArhCgHcVcyRO'
	]

	embed = discord.Embed(title=context.guild.name, description="Look at this cute dog", color=0x6A5ACD)
	embed.set_image(url=random.choice(dogList))
	await context.send(embed=embed)	
