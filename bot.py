#!/usr/bin/python3.7
import discord
import config
from datetime import datetime
import random

#https://discord.com/developers/applications
#https://discordpy.readthedocs.io/en/latest/api.html

TOKEN = config.DISCORD_TOKEN


client = discord.Client()

# login
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

starttime = datetime.now()

@client.event
async def on_message(message):
    # make sure the bot doesn't reply to itself
    if message.author == client.user:
        return
    
# simple if statements looking for specific text in messages
    if message.content == '!movies':
        #format the sheet embed
        sheet=discord.Embed(title="Movies Google Sheet", url=config.MOVIE_SHEET, description="Shared Google Sheet where we pick movies/shows to watch together.", color=0xFF5733)
        sheet.set_thumbnail(url="https://i.imgur.com/0hQyd5L.gif")
        await message.channel.send(embed = sheet)
        #format the calendar embed
        cal=discord.Embed(title="Movies Google Calendar", url=config.MOVIE_CALENDAR, description="Shared Google Calendar used to keep track of when we are watching movies/shows.", color=0xFF5733)
        cal.set_thumbnail(url="https://i.pinimg.com/originals/63/be/5f/63be5f30749ff7be7bb4a633ffac763f.gif")
        await message.channel.send(embed = cal)
        #format the calendar embed
        vote=discord.Embed(title="Movies Date Vote", url=config.MOVIE_VOTE, description="Vote for the next movie night date.", color=0xFF5733)
        vote.set_thumbnail(url="https://media2.giphy.com/media/55m7McmQ9tcD26kQ3I/giphy.gif?cid=ecf05e47u8ah5z3t5v5w6b9dyv8fipeu1jrtf84an19zuehy&rid=giphy.gif")
        await message.channel.send(embed = vote)

    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')
    if 'merry christmas' in message.content.lower():
        await message.channel.send('Merry Christmas! 🎄🎅')
    if message.content == '!shrug':
        await message.channel.send('¯\_(ツ)_/¯')
    if message.content == '!uptime':
        runtime = datetime.now()-starttime
        await message.channel.send(f"<@791794369824030781> has been running for: {runtime}")



    # reactions
    # if date is christmas, reply to every message with :santa:
    if (datetime.now().month == 12):
        emote = ['🎅','🎄','🎁','❄️','🤶','🧝','🌟','☃️','⛄','🔥','🔔','🎶','🕯️','🦌']
        await message.add_reaction(random.choice(emote))
    #poop
    if 'poo' in message.content.lower() or 'shit' in message.content.lower() or 'dump' in message.content.lower():
        await message.add_reaction('💩')





client.run(TOKEN)
#client.close()