import os
from datetime import datetime
import discord
from discord.ext import commands
import music
import requests
import time
import asyncio

client = commands.Bot(command_prefix=">", intents = discord.Intents.all())

cogs = [music]

welcome = f"""I'm Online Right Now.
Author: @iDead"""

channel1 = "851806673232199730"
channel2 = "905017361353035806"

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready():
    print('''Welcome to Discord Music Player Bot.
Logged in as {0.user}'''.format(client))
    ch1 = client.get_channel(channel1)
    ch2 = client.get_channel(channel2)
    await ch1.send(welcome)
    await ch1.send(f"Bot Latency: {round(client.latency * 1000)}ms")
    await ch2.send(welcome)
    await ch2.send(f"Bot Latency: {round(client.latency * 1000)}ms")

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
    time1 = datetime.now()
    time1utc = datetime.utcnow()
    titles = "Current Time (Local/UTC)"
    author = ctx.message.author.name
    
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

async def reminder():
    await client.wait_until_ready()
    ch1 = client.get_channel(channel1)
    ch2 = client.get_channel(channel2)
    hour = int(datetime.now().time().strftime("%H"))
    minute = int(datetime.now().time().strftime("%M"))
    if hour == 7:
        pagi1 = discord.Embed(
            title="--- AutoSend ---",
            description="Good Morning, everyone",
        )
        await ch1.send(embed=pagi1)
        await ch2.send(embed=pagi1)
    if hour == 11 and minute == 30:
        siang1 = discord.Embed(
            title="--- AutoSend ---",
            description="Good Afternoon, friends",
        )
        await ch1.send(embed=siang1)
        await ch2.send(embed=siang1)
    if hour == 19:
        malam1 = discord.Embed(
            title="--- AutoSend ---",
            description="Good Evening, Bois",
        )
        await ch1.send(embed=malam1)
        await ch2.send(embed=malam1)
    if hour = 23 and minute == 30:
        tengah_malam1 = discord.Embed(
            title="--- AutoSend ---",
            description="Good Night, everyone",
        )
        await ch1.send(embed=tengah_malam1)
        await ch2.send(embed=tengah_malam1)
    await asyncio.sleep(30)

client.loop.create_task(reminder())
client.run('OTA0MTU2MDI2ODUxNDU1MDA2.YX3a6w.8Bt_jbhu432HFbMjsc26BM53hjg')
