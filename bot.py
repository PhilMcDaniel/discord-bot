#!/usr/bin/python3.7
import discord
import datetime
import random
from discord.ext import commands
import asyncio
from decimal import *
import logging
import os

from rlrankparser import form_url,get_rank_from_api
import config
from openai_functions import *

# Get the directory containing the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# create logger so root is not used
logger = logging.getLogger('bot')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler(os.path.join(BASE_DIR, 'bot.log'))
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

class FileContentManager:
    def __init__(self):
        self.content_cache = {}
        
    def load_file(self, filename, process_line=None):
        """
        Loads a file into the cache with optional line processing
        
        Args:
            filename (str): Name of the file to load
            process_line (function, optional): Function to process each line. 
                                            Default processing strips whitespace.
        
        Returns:
            bool: True if file was loaded successfully, False otherwise
        """
        try:
            # Convert relative filename to absolute path
            filepath = os.path.join(BASE_DIR, filename)
            with open(filepath, "r", encoding="utf8") as file:
                if process_line is None:
                    process_line = lambda x: x.rstrip()
                
                self.content_cache[filename] = [process_line(line) for line in file]
                return True
        except Exception as e:
            logger.error(f"Error loading file {filepath}: {e}")
            self.content_cache[filename] = []
            return False
    
    def get_random_line(self, filename):
        """Gets a random line from the specified file's cached content"""
        if filename in self.content_cache and self.content_cache[filename]:
            return random.choice(self.content_cache[filename])
        return None
    
    def get_all_lines(self, filename):
        """Gets all lines from the specified file's cached content"""
        return self.content_cache.get(filename, [])

# Create an instance after bot initialization
file_manager = FileContentManager()

# Load the required files at startup
file_manager.load_file("jokes.txt", lambda x: x.rstrip().replace('\\n', '\n'))
file_manager.load_file("insults.txt")
file_manager.load_file("lore.txt")

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

@bot.command(name='joke', help="Replies back with a joke")
async def joke(ctx):
    d = {'command': '!joke'}
    try:
        response = file_manager.get_random_line("jokes.txt")
        if response:
            await ctx.send(response)
            logger.info('Command issued', extra=d)
        else:
            await ctx.send("Sorry, no jokes available right now!")
            logger.warning('No jokes available', extra=d)
    except Exception as e:
        logger.error(f'Error in joke command: {e}', extra=d)
        await ctx.send("Sorry, I'm having trouble telling jokes right now!")

@bot.command(name='poke', help="Gently prod a user")
async def poke(ctx, user):
    d = {'command': '!poke'}
    try:
        insult = file_manager.get_random_line("insults.txt")
        if insult:
            response = f"{user} - {insult}"
            await ctx.send(response)
            logger.info('Command issued', extra=d)
        else:
            await ctx.send(f"Sorry, I can't think of anything clever to say to {user} right now!")
            logger.warning('No insults available', extra=d)
    except Exception as e:
        logger.error(f'Error in poke command: {e}', extra=d)
        await ctx.send("Sorry, I'm having trouble poking right now!")

@bot.command(name='lore', help="Reaches through the annals of the historical record to return significant moments.")
async def lore(ctx):
    d = {'command': '!lore'}
    try:
        lines = file_manager.get_all_lines("lore.txt")
        for line in lines:
            await ctx.send(line)
        logger.info('Command issued', extra=d)
    except Exception as e:
        logger.error(f'Error in lore command: {e}', extra=d)
        await ctx.send("Sorry, the historical records are unavailable right now!")

@bot.command(name='addtobot',help='EX: !addtobot "add your suggestion here" ')    
async def addsugg(ctx,suggestion):
    d = {'command':'!suggestion'}
    suggestions_path = os.path.join(BASE_DIR, "suggestions.txt")
    with open(suggestions_path, 'a') as file_object:
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

bot.run(TOKEN)