#!/usr/bin/python3.7
import discord
import datetime
import random
from discord.ext import commands
import atexit
from decimal import *
import logging
import os

from rlrankparser import form_url,get_rank_from_api
import config
from openai_functions import *

# create logger so root is not used
logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('bot.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
#d stores key value extra data to log
d = {'command':'NA'}
formatter = logging.Formatter('%(asctime)s,%(levelname)s,%(command)s,%(message)s',datefmt='%Y-%m-%d %H:%M:%S')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

#disable/enable logging here
logger.disabled = False


getcontext().prec = 15

#https://discord.com/developers/applications
#https://discordpy.readthedocs.io/en/latest/api.html

TOKEN = config.DISCORD_TOKEN

intents = discord.Intents.all()

bot = commands.Bot(command_prefix='!', intents=intents)


# login
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    logger.info(f'{bot.user.name} has connected to Discord!',extra=d)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="commands from my human masters"))
starttime = datetime.datetime.now()

#commands

@bot.command(name='shrug',help=r'¯\_(ツ)_/¯')
async def shrug(ctx):
    d = {'command':'!shrug'}
    response = r'¯\_(ツ)_/¯'
    await ctx.send(response)
    logger.info(f'Command issued',extra=d)

@bot.command(name='playcsgo',help=r'Add bot to team in CS:GO')
async def playcsgo(ctx):
    d = {'command':'!playcsgo'}
    messageuserid = ctx.message.author.id
    response = f"I'm sorry <@{messageuserid}>, but based on my records it looks like your rank is too low to queue together. Please try again after you get gud."
    await ctx.send(response)
    logger.info(f'Command issued',extra=d)

@bot.command(name='uptime',help='How long has the bot currently been running')
async def uptime(ctx):
    d = {'command':'!uptime'}
    #get old uptime
    with open("uptime.txt",'r') as file:
        olduptime = int(file.readline())
    #get current delta
    deltaseconds = int((datetime.datetime.now()-starttime).total_seconds())
    deltatime = datetime.timedelta(seconds = deltaseconds)
    #add old plus delta to get new
    newuptime = datetime.timedelta(seconds=int(olduptime+deltaseconds))
    response = f"Current uptime for <@791794369824030781> is: {deltatime}. Overall uptime is {newuptime}"
    await ctx.send(response)
    logger.info(f'Command issued',extra=d)

@bot.command(name='poke',help="Gently prod a user")
async def poke(ctx,user):
    d = {'command':'!poke'}
    with open("insults.txt",encoding="utf8") as file_object:
        lines = file_object.readlines()
    for line in lines:
        line = line.rstrip()
    randominsult = random.choice(lines)
    response = f"{user} - {randominsult}"
    await ctx.send(response)
    logger.info(f'Command issued',extra=d)


@bot.command(name='joke',help="Replies back with a joke")
async def joke(ctx):
    d = {'command':'!joke'}
    escapedlist = []
    with open("jokes.txt",encoding="utf8") as file_object:
        lines = file_object.readlines()
    for line in lines:
       line = line.rstrip()
       #there is an extra \ infront of \n so I'm manually removing it.
       line = line.replace('\\n', '\n')
       escapedlist.append(line)
    randomjoke = random.choice(escapedlist)
    response = f"{randomjoke}"
    await ctx.send(response)
    logger.info(f'Command issued',extra=d)


@bot.command(name='addtobot',help='EX: !addtobot "add your suggestion here" ')    
async def addsugg(ctx,suggestion):
    d = {'command':'!suggestion'}
    with open("suggestions.txt",'a') as file_object:
        file_object.write(f"{suggestion}\n")
    await ctx.send(f"Suggestion added: {suggestion}")
    logger.info(f'Command issued',extra=d)

@bot.command(name='rlrank',help='Returns Rocket League ranks. !rlrank platform platformid')
async def getrlrank(ctx,platform,platformid):
    d = {'command':'!rlrank'}
    #store list of ratings from scraping in list
    resp_list = get_rank_from_api(form_url(platform,platformid))
    #send message for each rating
    for resp in resp_list:
        await ctx.send(resp)
    logger.info(f'Command issued',extra=d)


@bot.command(name='aitext',help='Calls the OpenAI text completion api with the user provided prompt.')
async def aitext(ctx,text_prompt):
    d = {'command':'!aitext'}
    try:
        openai_response = get_aitext_completion(text_prompt)
        #split because discord can only send 2000 character messages
        split_response = split_at_punctuation(openai_response)
        for chunk in split_response:
            await ctx.send(chunk)
    except Exception as e:
        await ctx.send(f"There was an issue sending the request to openai. Error: :{e}")
        logger.info(f"OpenAI error: {e}")
    logger.info(f'Command issued',extra=d)

@bot.command(name='aiimage',help='Calls the OpenAI image generation api with the user provided prompt.')
async def aiimage(ctx,text_prompt):
    d = {'command':'!aiimage'}
    try:
        image_url = get_aiimage(text_prompt)
        await ctx.send(image_url)
    except Exception as e:
        await ctx.send(f"There was an issue sending the request to openai. Error: :{e}")
        logger.info(f"OpenAI error: {e}")
    logger.info(f'Command issued',extra=d)

@bot.command(name='rng',help='Returns a series of random numbers. !rng 3 1 6 returns 3 random numbers between 1 and 6')
async def random_numbers(ctx,amount,min,max):
    d = {'command':'!rng'}
    total = 0
    numbers=[]
    if int(amount) <= 1000 and int(amount) >= 1:
        for x in range(1,int(amount)+1):
            value = (random.randint(int(min),int(max)))
            numbers.append(value)
            total = total + value
        await ctx.send(f"{numbers} Total = {total}")
    else:
        await ctx.send(f"Please choose an amount of numbers between 1 and 1000")
    logger.info(f'Command issued',extra=d)

@bot.command(name='lore',help="Reaches through the annals of the historical record to return significant moments.")
async def lore(ctx):
    d = {'command':'!lore'}
    with open("lore.txt",encoding="utf8") as file_object:
        lines = file_object.readlines()
    for line in lines:
        line = line.rstrip()
        await ctx.send(line)
    logger.info(f'Command issued',extra=d)

#message reply/reaction
@bot.event
async def on_message(message):
    try:
    # make sure the bot doesn't reply to itself
        if message.author == bot.user:
            return

        if 'happy birthday' in message.content.lower():
            await message.channel.send('Happy Birthday! 🎈🎉')
        if 'merry christmas' in message.content.lower():
            await message.channel.send('Merry Christmas! 🎄🎅')

        # reactions
        # if date is christmas, reply to every message with :santa:
        if (datetime.datetime.now().month == 12):
            emote = ['🎅','🎄','🎁','❄️','🤶','🧝','🌟','☃️','⛄','🔥','🔔','🎶','🕯️','🦌']
            await message.add_reaction(random.choice(emote))
        #poop
        if 'poo' in message.content.lower() or 'shit' in message.content.lower() or 'dump' in message.content.lower():
            await message.add_reaction('💩')

        #this is needed for the commands to work appropriately https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working
        await bot.process_commands(message)
    except Exception as e:
        logger.info(f"error in on_message, {e}")

#write new uptime to file
def updateuptime():
    with open("uptime.txt",'r') as file:
        olduptime = int(file.readline())
        deltaseconds = int((datetime.datetime.now()-starttime).total_seconds())
        
        #add old plus delta to get new
        newuptimeseconds = olduptime + deltaseconds
    
    with open("uptime.txt", "w") as outfile:
        outfile.write(str(newuptimeseconds))

atexit.register(updateuptime)

bot.run(TOKEN)