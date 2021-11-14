import os
from datetime import datetime
import discord
from discord.ext import commands
import music
import json
import pytz
import requests
import time
import asyncio

client = commands.Bot(command_prefix=">", intents = discord.Intents.all())

cogs = [music]

welcome = f"""I'm Online Right Now.
Author: @iDead"""

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event #bot_event
async def on_ready():
    print('''Welcome to Discord Music Player Bot.
Logged in as {0.user}'''.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))
    ch1 = client.get_channel(851806673232199730)
    ch2 = client.get_channel(905017361353035806)
    await ch1.send(welcome)
    await ch1.send(f"Bot Latency: {round(client.latency * 1000)}ms")
    await ch2.send(welcome)
    await ch2.send(f"Bot Latency: {round(client.latency * 1000)}ms")

@client.command()
async def hentai(ctx):
    """Uncensored Anime Image (18+ Warning)"""
    chid = client.get_channel(909283710665379911)
    
    async with ctx.typing():
        if ctx.channel.id is not chid.id:
            await ctx.send('Write this command in {}'.format(chid.mention))
    
        url1 = "https://api.waifu.pics/nsfw/waifu"
        url2 = "https://api.waifu.pics/nsfw/neko"
        url3 = "https://api.waifu.pics/nsfw/blowjob"
        author = ctx.message.author.mention
        r1 = requests.get(url1)
        r2 = requests.get(url2)
        r3 = requests.get(url3)
        data1 = r1.json()
        data2 = r2.json()
        data3 = r3.json()
        img_url1 = data1['url']
        img_url2 = data2['url']
        img_url3 = data3['url']
        randimg = random.choice(img_url1, img_url2, img_url3)
        embed = discord.Embed(
            title="--- 18+ Hentai Image ---"
            description=f"Are you satisfied, {author}"
        )
        embed.set_image(url=randimg)
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=embed)

@client.command()
async def waifu(ctx):
    """Waifu images for you"""
    url = "https://api.waifu.pics/sfw/waifu"
    author = ctx.message.author.mention
    r = requests.get(url)
    data = r.json()
    img_url = data['url']
    embed = discord.Embed(
        title="--- Random Waifu Images ---",
        description=f"Waifu for {author}",
    )
    embed.set_image(url=img_url)
    embed.set_footer(text="Requested by {}".format(author), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

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

@client.command() #current_time
async def time(ctx):
    """Showing Current Time (Local/UTC)"""
    time1 = datetime.now(pytz.timezone('Asia/Jakarta'))
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

@client.command(name="avatar") #avatar_command
async def avatar_(ctx, avamem : discord.Member=None):
    """Get Avatar Image from Specified User"""
    if avamem is None:
        avamem = ctx.author
    useravatar = avamem.avatar_url
    author = ctx.message.author.name
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- Avatar ---",
        description=f"{avamem.mention} Avatar",
    )
    embed.set_image(url=useravatar)
    embed.set_footer(text="Requested by {}".format(author), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

client.run('OTA0MTU2MDI2ODUxNDU1MDA2.YX3a6w.5MpGgosOjwIYlz0iXFPSTVPwyqI')
