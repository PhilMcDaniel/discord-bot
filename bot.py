#!/usr/bin/python3.7
import discord
import datetime
import random
from discord.ext import commands
import atexit
from decimal import *
import logging
import openai
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
@bot.command(name='movies',help='Links for movie night coordination. See "movie-night" channel for more info')
async def movies(ctx):
    d = {'command':'!movies'}
    #format the sheet embed
    sheet=discord.Embed(title="Movies Google Sheet", url=config.MOVIE_SHEET, description="Shared Google Sheet where we pick movies/shows to watch together.", color=0xFF5733)
    sheet.set_thumbnail(url="https://i.imgur.com/0hQyd5L.gif")
    #format the calendar embed
    cal=discord.Embed(title="Movies Google Calendar", url=config.MOVIE_CALENDAR, description="Shared Google Calendar used to keep track of when we are watching movies/shows.", color=0xFF5733)
    cal.set_thumbnail(url="https://i.pinimg.com/originals/63/be/5f/63be5f30749ff7be7bb4a633ffac763f.gif")

    #format the calendar embed
    vote=discord.Embed(title="Movies Date Vote", url=config.MOVIE_VOTE, description="Vote for the next movie night date.", color=0xFF5733)
    vote.set_thumbnail(url="https://media2.giphy.com/media/55m7McmQ9tcD26kQ3I/giphy.gif?cid=ecf05e47u8ah5z3t5v5w6b9dyv8fipeu1jrtf84an19zuehy&rid=giphy.gif")

    await ctx.send(embed = sheet)
    await ctx.send(embed = cal)
    await ctx.send(embed = vote)
    logger.info(f'Command issued',extra=d)

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

@bot.command(name='aiart',help='Returns ai art from OpenAI based on prompt')
async def aiart(ctx,text_prompt):
    d = {'command':'!aiart'}
    try:
        await ctx.send("OpenAI moderation category results\n")
        #category scores
        for key, value in get_moderation_category_scores(text_prompt).items():
            await ctx.send(f"\t - Category: {key}, score: {format(value,'.4f')}")
    except:
        pass
    try:
        for resp in get_aiart(text_prompt):
            await ctx.send(resp['url'])
    except openai.InvalidRequestError:
        await ctx.send("Your prompt contained text that was not allowed by the openai safety system.")
    logger.info(f'Command issued',extra=d)

@bot.command(name='aitext',help='Replies back in an intelligent manner based on prompt')
async def aiart(ctx,text_prompt):
    d = {'command':'!aitext'}
    try:
        await ctx.send("OpenAI moderation category results\n")
        #category scores
        for key, value in get_moderation_category_scores(text_prompt).items():
            await ctx.send(f"\t - Category: {key}, score: {format(value,'.4f')}")
    except:
        pass
    try:
        await ctx.send("\n\nRESULT:\n")
        await ctx.send(get_aitext_completion(text_prompt))
    except openai.InvalidRequestError:
        await ctx.send("Your prompt contained text that was not allowed by the openai safety system.")    
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

#message reply/reaction
@bot.event
async def on_message(message):
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