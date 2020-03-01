import random
import discord
from config.setup  import bot

@bot.command(pass_context=True)
async def cat(context):
	catList =[
		'https://giphy.com/gifs/funny-cat-mlvseq9yvZhba',
		'https://giphy.com/gifs/JIX9t2j0ZTN9S',
		'https://giphy.com/gifs/leroypatterson-cat-glasses-CjmvTCZf2U3p09Cn0h',
		'https://giphy.com/gifs/cat-funny-WXB88TeARFVvi',
		'https://giphy.com/gifs/tiktok-aww-hTgmFytUwwHLaMahU1',
		'https://giphy.com/gifs/cat-bye-er19eYafoFxrq',
		'https://giphy.com/gifs/C9x8gX02SnMIoAClXa',
		'https://giphy.com/gifs/reaction-Nm8ZPAGOwZUQM',
		'https://giphy.com/gifs/cat-kisses-hugs-MDJ9IbxxvDUQM',
		'https://giphy.com/gifs/animals-being-jerks-xtGpIp4ixR6Gk',
		'https://giphy.com/gifs/aww-11s7Ke7jcNxCHS',
		'https://giphy.com/gifs/transparent-baby-shake-nNxT5qXR02FOM',
		'https://giphy.com/gifs/cat-moment-remember-8vQSQ3cNXuDGo',
		'https://giphy.com/gifs/cat-humour-funny-ICOgUNjpvO0PC',
		'https://giphy.com/gifs/cat-weird-bra-p4xp4BjHIdane',
		'https://giphy.com/gifs/banggood-cat-pets-dacing-xJjs8eGVbjNYY',
		'https://giphy.com/gifs/kitty-smart-1iu8uG2cjYFZS6wTxv',
		'https://giphy.com/gifs/funny-efHwZH4DeN9ss',
		'https://giphy.com/gifs/cheezburger-cat-mountain-good-job-fXgKfzV4aaHQI',
		'https://giphy.com/gifs/cat-adorable-cuddle-PibhPmQYXZ7HO',
		'https://giphy.com/gifs/weinventyou-3rgXBN6i9LIUg6lSLe',
		'https://giphy.com/gifs/ign-describe-plans-13HBDT4QSTpveU',
		'https://giphy.com/gifs/tT0wtdSJvE0Rq',
		'https://giphy.com/gifs/Lp5wuqMOmLUaAd0jBG',
		'https://giphy.com/gifs/cat-lasers-cucumber-3oEduQAsYcJKQH2XsI',
		'https://giphy.com/gifs/cat-i-cant-mo8MAe2maHrva',
		'https://giphy.com/gifs/cheezburger-cat-kittens-dj-t7MWRoExDRF72',
		'https://giphy.com/gifs/cat-box-legs-10SAlsUFbyl5Dy',
		'https://giphy.com/gifs/8cErt0PCSgzOY375br',
		'https://giphy.com/gifs/cat-fail-fat-lN9amhr8GZMhG',
		'https://giphy.com/gifs/cat-kitten-kids-Q56ZI04r6CakM',
		'https://giphy.com/gifs/funny-cat-gato-gatos-tBxyh2hbwMiqc',
		'https://giphy.com/gifs/cat-walking-table-vlUCWLGF7jpwA',
		'https://giphy.com/gifs/Zdfwny4fjIu2s',
		'https://giphy.com/gifs/cat-cute-trippy-26xBEez1vnVb2WgBq',
		'https://giphy.com/gifs/cat-spinning-roomba-qoxM1gi6i0V9e',
		'https://giphy.com/gifs/9VgB7x6yTpvOMHauzh',
		'https://giphy.com/gifs/v6aOjy0Qo1fIA',
		'https://giphy.com/gifs/cute-aww-eyebleach-LYd7VuYqXokv20CaEG',
		'https://giphy.com/gifs/reaction-mood-3dpGaQxDQthaQDeWFF',
		'https://giphy.com/gifs/cat-fluffy-XMxPoXBNpjrRC',
		'https://giphy.com/gifs/cat-disney-sad-pncpd012ij3qw',
		'https://giphy.com/gifs/82CItLnbSh8hzsXK3H',
		'https://giphy.com/gifs/loop-cat-EmMWgjxt6HqXC',
		'https://giphy.com/gifs/1PgFpz0u4diQRuHyvE',
		'https://giphy.com/gifs/23eIaihzejUmUtIDkO',
		'https://giphy.com/gifs/cat-loop-exercise-hpJOl7t4qeh5m',
		'https://giphy.com/gifs/cat-cute-roomba-3iBcRAErFhFwoTVbN5',
		'https://giphy.com/gifs/b5XJRNBrvgVHjkTsRV',
		'https://giphy.com/gifs/cat-fat-crunches-KgcjJH2LgCmMo',
		'https://giphy.com/gifs/viralhog-funny-cat-cute-4QFzZTjadMFPynIRea',
		'https://giphy.com/gifs/cat-cute-box-hGLdrItUOxou4',
		'https://giphy.com/gifs/d3zUEBN9RdNE4',
		'https://giphy.com/gifs/cat-turtle-eY2Q6hxp1ZeFi',
		'https://giphy.com/gifs/tkM2AQZpPCDhC',
		'https://giphy.com/gifs/cat-back-pig-6ureN5mMrHAxq',
		'https://giphy.com/gifs/cat-skateboard-fSbYwraWQuCKQ',
		'https://giphy.com/gifs/cat-maru-loop-Mhy9hKgfwI0lG'
	]

	embed = discord.Embed(title=context.guild.name, description="Look at this cute cat", color=0x6A5ACD)
	embed.set_image(url=random.choice(catList))
	await context.send(embed=embed)	

