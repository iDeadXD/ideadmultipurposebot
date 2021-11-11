import os
from datetime import datetime
import discord
from discord.ext import commands
import music
import requests
import asyncio

client = commands.Bot(command_prefix=">", intents = discord.Intents.all())

cogs = [music]

welcome = f"""I'm Online Right Now.
Author: @iDead"""

pagi = discord.Embed(
    title="--- AutoSend ---",
    description="Good Morning, everyone",
)
siang = discord.Embed(
    title="--- AutoSend ---",
    description="Good Afternoon, friends",
)
malam = discord.Embed(
    title="--- AutoSend ---",
    description="Good Evening, Bois",
)
tengah_malam = discord.Embed(
    title="--- AutoSend ---",
    description="Good Night, everyone",
)

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event
async def on_ready():
    print('''Welcome to Discord Music Player Bot.
Logged in as {0.user}'''.format(client))
    current_time = datetime.utcnow().strftime("%H:%M")
    channel1 = client.get_channel(851806673232199730)
    channel2 = client.get_channel(905017361353035806)
    await channel1.send(welcome)
    await channel1.send(f"Bot Latency: {round(client.latency * 1000)}ms")
    await channel2.send(welcome)
    await channel2.send(f"Bot Latency: {round(client.latency * 1000)}ms")
    
    if current_time == "07:00":
        await channel1.send(embed=pagi)
        await channel2.send(embed=pagi)
    elif current_time == "11:00":
        await channel1.send(embed=siang)
        await channel2.send(embed=siang)
    elif current_time == "19:00":
        await channel1.send(embed=malam)
        await channel2.send(embed=malam)
    elif current_time == "23:00":
        await channel1.send(embed=tengah_malam)
        await channel2.send(embed=tengah_malam)

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
