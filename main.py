import os
from datetime import datetime
import discord
from discord.ext import commands
import music
import random
import json
import pytz
import requests
import time
import asyncio
from config import CONFIG
from imgapi import SFW, NSFW
from msg_channel import CHANNEL

client = commands.Bot(command_prefix=CONFIG['prefix'], intents = discord.Intents.all())

cogs = [music]

welcome = f"""I'm Online Right Now.
Author: iDead#9496."""

for i in range(len(cogs)):
    cogs[i].setup(client)

@client.event #bot_event
async def on_ready():
    print('''Welcome to Discord Music Player Bot.
Logged in as {0.user}'''.format(client))
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))
    ch1 = client.get_channel(int(CHANNEL['channel1']))
    ch2 = client.get_channel(int(CHANNEL['channel2']))
    await ch1.send(welcome + f" Bot Latency: {round(client.latency * 1000)}ms")
    await ch2.send(welcome + f" Bot Latency: {round(client.latency * 1000)}ms")

@client.command()
async def waifu(ctx, member : discord.Member=None):
    """Waifu Image for You"""
    
    async with ctx.typing():
        if member is None:
            member = ctx.author
        if ctx.channel.is_nsfw():
            await ctx.send('Note: Write this command outside the NSFW channel')
            return
        url = SFW['waifu1']
        r = requests.get(url)
        data = r.json()
        img_url = data['url']
        desc1 = [
            f"Do you love me, {member.mention}?",
            f"I love you, {member.mention}",
            f"Do you love her, {member.mention}?",
            f"Do you want her to be your girlfriend, {member.mention}?",
            f"Please make me your bride, {member.mention}",
            f"Take her to dinner, {author}",
            f"I will be your girlfriend, {member.mention}",
            f"Hey, {member.mention}. Can you give me some love?",
            f"Hey {member.mention}, you're my boyfriend right?",
            f"She's your girlfriend right, {member.mention}?",
        ]
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Random Waifu Image ---",
            description=random.choice(desc1)
        )
        embed.set_image(url=img_url)
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=embed)

@client.command()
async def hentai(ctx):
    """Uncensored Anime Image (18+ Warning)"""
    async with ctx.typing():
        if ctx.channel.is_nsfw():
            url1 = NSFW['hentai1']
            url2 = NSFW['hentai2']
            url3 = NSFW['hentai3']
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
            imgdata = [
                img_url1,
                img_url2,
                img_url3,
            ]
            titles = [
                f"Are you satisfied, {author}",
                f"You're horny right?, {author}",
                f"I think, you're pervert {author}",
                f"You got a good one, {author}"
            ]
            embed = discord.Embed(
                title="--- 18+ Hentai Image ---",
                description=random.choice(titles),
            )
            embed.set_image(url=random.choice(imgdata))
            embed.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send('Note: Write this command in NSFW channel')

@client.command()
async def slap(ctx, member : discord.Member=None):
    if member is None:
        member = ctx.author
    url4 = SFW['slap1']
    r4 = requests.get(url4)
    data4 = r4.json()
    imgdata = data4['url']
    author = ctx.message.author.mention
    desc = [
        f"{author} slapped {member.mention}",
        f"{author}: I got you, {member.mention}",
    ]
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- Slap Someone ---",
        description=random.choice(desc),
    )
    embed.set_image(url=imgdata)
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
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- Avatar ---",
        description=f"{avamem.mention} Profile Avatar",
    )
    embed.set_image(url=useravatar)
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

client.run(CONFIG['token'])
