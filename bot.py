import discord
import config


#https://discord.com/developers/applications
#https://discordpy.readthedocs.io/en/latest/api.html

TOKEN = config.DISCORD_TOKEN


client = discord.Client()

# login
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    # make sure the bot doesn't reply to itself
    if message.author == client.user:
        return
    
# simple if statements looking for specific text in messages
    if message.content == '!movies':
        await message.channel.send(config.MOVIES_LINK)
    if message.content == '!erotica':
        await message.channel.send(f'Here you go, {message.author} - https://www.reddit.com/r/Erotica/')
    if 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')
    if message.content == '!shrug':
        await message.channel.send('¯\_(ツ)_/¯')
client.run(TOKEN)
#client.close()