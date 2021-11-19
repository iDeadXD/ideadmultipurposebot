import os
from datetime import datetime
import discord
from discord.ext import commands
import music
import imgcogs
import helper
import random
import json
import pytz
import requests
import time
import asyncio
from config import CONFIG
from imgapi import WELCOME
from msg_channel import CHANNEL
from custom_msg import J_MESSAGE

client = commands.Bot(command_prefix=CONFIG['prefix'], intents = discord.Intents.all())

cogs = [music]
cogs1 = [imgcogs]
cogs2 = [helper]

welcome = f"""I'm Online Right Now.
Author: iDead#9496."""

for i in range(len(cogs)):
    cogs[i].setup(client)

for i in range(len(cogs1)):
    cogs1[i].setup(client)

for i in range(len(cogs2)):
    cogs2[i].setup(client)

@client.event #bot_event
async def on_ready():
    print('''Welcome to Discord Music Player Bot.
Logged in as {0.user}'''.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))
    ch1 = client.get_channel(int(CHANNEL['channel1']))
    ch2 = client.get_channel(int(CHANNEL['channel2']))
    await ch1.send(welcome + f" Bot Latency: {round(client.latency * 1000)}ms")
    await ch2.send(welcome + f" Bot Latency: {round(client.latency * 1000)}ms")

@client.event #Send message when someone join
async def on_member_join(member):
    ch3 = client.get_channel(int(CHANNEL['channel4']))
    guild = member.guild
    desc = [
        str(J_MESSAGE['j_msg1']).format(member.mention, guild),
        str(J_MESSAGE['j_msg2']).format(guild, member.mention),
        str(J_MESSAGE['j_msg3']).format(guild, member.mention)
    ]
    
    imgdata = [
        str(WELCOME['welcome1']),
        str(WELCOME['welcome2']),
        str(WELCOME['welcome3']),
        str(WELCOME['welcome4'])
    ]
    
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- New Member Join!! ---",
        desc=random.choice(desc)
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_image(url=random.choice(imgdata))
    embed.set_footer(text="Joined on: Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")))
    
    await ch3.send(embed=embed)

client.run(CONFIG['token'])
