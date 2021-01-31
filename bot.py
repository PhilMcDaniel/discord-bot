#!/usr/bin/python3.7
import discord
import config
import datetime
import random
from discord.ext import commands
import atexit
from decimal import *

getcontext().prec = 15

#https://discord.com/developers/applications
#https://discordpy.readthedocs.io/en/latest/api.html

TOKEN = config.DISCORD_TOKEN


intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

# login
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="commands from my human masters"))
starttime = datetime.datetime.now()

#commands
@bot.command(name='movies',help='Links for movie night coordination. See "movie-night" channel for more info')
async def movies(ctx):
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

@bot.command(name='shrug',help=r'¯\_(ツ)_/¯')
async def shrug(ctx):
    response = r'¯\_(ツ)_/¯'
    await ctx.send(response)

@bot.command(name='playcsgo',help=r'Add bot to team in CS:GO')
async def playcsgo(ctx):
    messageuserid = ctx.message.author.id
    response = f"I'm sorry <@{messageuserid}>, but based on my records it looks like your rank is too low to queue together. Please try again after you get gud."
    await ctx.send(response)

@bot.command(name='uptime',help='How long has the bot currently been running')
async def uptime(ctx):
    #get old uptime
    with open("uptime.txt",'r') as file:
        olduptime = int(file.readline())
    #get current delta
    deltaseconds = int((datetime.datetime.now()-starttime).total_seconds())
    deltatime = datetime.timedelta(seconds = deltaseconds)
    #add old plus delta to get new
    newuptime = datetime.timedelta(seconds=int(olduptime+deltaseconds))
    response = f"Current uptime for <@791794369824030781> is: {deltatime}. Overall uptime is {newuptime}"
    print(olduptime+deltaseconds)
    await ctx.send(response)

@bot.command(name='poke',help="Gently prod a user")
async def poke(ctx,user):
    with open("insults.txt",encoding="utf8") as file_object:
        lines = file_object.readlines()
    for line in lines:
        line = line.rstrip()
    randominsult = random.choice(lines)
    response = f"{user} - {randominsult}"
    await ctx.send(response)


@bot.command(name='joke',help="Replies back with a joke")
async def joke(ctx):
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
    #print(response)
    await ctx.send(response)


@bot.command(name='addtobot',help='EX: !addtobot "add your suggestion here" ')    
async def addsugg(ctx,suggestion):
    with open("suggestions.txt",'a') as file_object:
        file_object.write(f"{suggestion}\n")
    await ctx.send(f"Suggestion added: {suggestion}")


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