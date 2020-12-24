import discord
import config

#https://discord.com/developers/applications
#https://discordpy.readthedocs.io/en/latest/api.html

TOKEN = config.DISCORD_TOKEN
#client.close()
client = discord.Client()


@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

client.run(TOKEN)
#client.close()