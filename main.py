import os
import discord
from discord.ext import commands
import music
import levelsystem
import voice_temp
import moderation
import utils
from config import CONFIG
from msg_channel import CHANNEL

client = commands.Bot(command_prefix=[CONFIG['default_prfx']], intents = discord.Intents.all())

#=== Cog List ===
cogs = [music]
cogs2 = [levelsystem]
cogs3 = [voice_temp]
cogs4 = [moderation]
cogs5 = [utils]

welcome = f"""I'm Online Right Now.
Author: iDead#9496."""

#=== Cog Executor ===
for i in range(len(cogs)):
    cogs[i].setup(client)

for i in range(len(cogs2)):
    cogs2[i].setup(client)

for i in range(len(cogs3)):
    cogs3[i].setup(client)

for i in range(len(cogs4)):
    cogs4[i].setup(client)

for i in range(len(cogs5)):
    cogs5[i].setup(client)

#=== Client Event Executor ===
@client.event #bot_event
async def on_ready():
    print('''Welcome to Discord Music Player Bot.
Logged in as {0.user}'''.format(client))
    ch1 = client.get_channel(int(CHANNEL['channel1']))
    ch2 = client.get_channel(int(CHANNEL['channel2']))
    await ch1.send(welcome + f" Bot Latency: {round(client.latency * 1000)}ms")
    await ch2.send(welcome + f" Bot Latency: {round(client.latency * 1000)}ms")

@client.event
async def on_guild_join(guild):
    current_guilds = len(client.guilds)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"in **{current_guilds}** **servers** | prefix >"))

@client.event
async def on_guild_remove(guild):
    current_guilds = len(client.guilds)
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"in **{current_guilds}** **servers** | prefix >"))

#=== Client Executor ===
client.run(CONFIG['token'])
