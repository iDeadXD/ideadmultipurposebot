import os
import discord
import datetime
from discord.ext import commands
import music
import requests
import asyncio

client = commands.Bot(command_prefix=">", intents = discord.Intents.all())

cogs = [music]

welcome = f"""I'm Online Right Now.
Author: @iDead"""

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready():
    print('''Welcome to Discord Music Player Bot.
Logged in as {0.user}'''.format(client))
    channel1 = client.get_channel(851806673232199730)
    channel2 = client.get_channel(905017361353035806)
    await channel1.send(welcome)
    await channel1.send(f"Bot Latency: {round(client.latency * 1000)}ms")
    await channel2.send(welcome)
    await channel2.send(f"Bot Latency: {round(client.latency * 1000)}ms")

@client.command() #ping
async def ping(ctx):
    """Showing Bot Latency and YouTube Server Status"""
    pings = requests.get("https://youtube.com")
    titles = "Pong!!"
    selflatency = str(f" {round(client.latency * 1000)}ms")
    ytlatency = str(f" {pings}")
    author = ctx.message.author.name
    embed = discord.Embed(
        title=titles,
    )
    embed.add_field(name="Your Latency", value=selflatency)
    embed.add_field(name="YouTube Server Status", value=ytlatency)
    embed.set_footer(text="Author: {}".format(author), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

@client.command()
async def time(ctx):
    time1 = datetime.datetime.now()
    time1utc = datetime.utcnow()
    titles = "Current Time (Local/UTC)"
    
    embed = discord.Embed(
        title=titles,
    )
    embed.add_field(name="Local Time", value=time1)
    embed.add_field(name="UTC Time", value=time1utc)
    embed.set_footer(text="Author: {}".format(author), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

@client.command() #supported_link
async def supported(ctx):
    """Checking supported music links"""
    titles = "Supported Platform for Music Player"
    desc = "For Now, Only Support YouTube Link"
    author = ctx.message.author.name
    embed = discord.Embed(
        title=titles,
        description=desc,
    )
    embed.set_footer(text="Author: {}".format(author), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

client.run('OTA0MTU2MDI2ODUxNDU1MDA2.YX3a6w.8Bt_jbhu432HFbMjsc26BM53hjg')
