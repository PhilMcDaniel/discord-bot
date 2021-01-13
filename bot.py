#!/usr/bin/python3.7
import discord
import config
from datetime import datetime
import random
from discord.ext import commands

#https://discord.com/developers/applications
#https://discordpy.readthedocs.io/en/latest/api.html

TOKEN = config.DISCORD_TOKEN


intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

# login
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

starttime = datetime.now()

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

@bot.command(name='shrug')
async def shrug(ctx):
    response = '¯\_(ツ)_/¯'
    await ctx.send(response)

@bot.command(name='uptime',help='How long has the bot currently been running')    
async def uptime(ctx):
    runtime = datetime.now()-starttime
    response = f"<@791794369824030781> has been running for: {runtime}"
    await ctx.send(response)

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
    if (datetime.now().month == 12):
        emote = ['🎅','🎄','🎁','❄️','🤶','🧝','🌟','☃️','⛄','🔥','🔔','🎶','🕯️','🦌']
        await message.add_reaction(random.choice(emote))
    #poop
    if 'poo' in message.content.lower() or 'shit' in message.content.lower() or 'dump' in message.content.lower():
        await message.add_reaction('💩')

    #this is needed for the commands to work appropriately https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working
    await bot.process_commands(message)

bot.run(TOKEN)