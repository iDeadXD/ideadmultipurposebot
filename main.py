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
from googleapiclient.discovery import build
from config import CONFIG
from imgapi import SFW, NSFW, MEME
from msg_channel import CHANNEL
from custom_msg import W_MESSAGE, H_MESSAGE, B_MESSAGE, S_MESSAGE, M_MESSAGE

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
    ch3 = client.get_channel(int(CHANNEL['channel3']))
    if ctx.channel is not ch3:
        await ctx.send("Note: Write this command in {}".format(ch3.mention))
        return
    
    if member is None:
        member = ctx.author
    if ctx.channel.is_nsfw():
        await ctx.send('Note: Write this command outside the NSFW channel')
        return
    url = SFW['waifu1']
    r = requests.get(url)
    data = r.json()
    img_url = data['url']
    desc = [
        str(W_MESSAGE['w_msg1']).format(member.mention),
        str(W_MESSAGE['w_msg2']).format(member.mention),
        str(W_MESSAGE['w_msg3']).format(member.mention),
        str(W_MESSAGE['w_msg4']).format(member.mention),
        str(W_MESSAGE['w_msg5']).format(member.mention),
        str(W_MESSAGE['w_msg6']).format(member.mention),
        str(W_MESSAGE['w_msg7']).format(member.mention),
        str(W_MESSAGE['w_msg8']).format(member.mention),
        str(W_MESSAGE['w_msg9']).format(member.mention),
        str(W_MESSAGE['w_msg10']).format(member.mention)
    ]
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- Random Waifu Image ---",
        description=random.choice(desc)
    )
    embed.set_image(url=img_url)
    embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
    await ctx.send(embed=embed)

@client.command()
async def hentai(ctx):
    """Hentai Anime Image (18+ Warning)"""
    if ctx.channel.is_nsfw():
        url1 = NSFW['hentai1']
        url2 = NSFW['hentai2']
        url3 = NSFW['hentai3']
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
        desc = [
            str(H_MESSAGE['h_msg1']).format(ctx.message.author.mention),
            str(H_MESSAGE['h_msg2']).format(ctx.message.author.mention),
            str(H_MESSAGE['h_msg3']).format(ctx.message.author.mention),
            str(H_MESSAGE['h_msg4']).format(ctx.message.author.mention),
        ]
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- 18+ Hentai Image ---",
            description=random.choice(desc),
        )
        embed.set_image(url=random.choice(imgdata))
        embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
    else:
        await ctx.send('Note: Write this command in NSFW channel')

@client.command()
async def slap(ctx, member : discord.Member=None):
    """Slaps your friend or yourself"""
    if member is None:
        member = ctx.author
    url4 = SFW['slap1']
    r4 = requests.get(url4)
    data4 = r4.json()
    imgdata = data4['url']
    desc = [
        str(S_MESSAGE['s_msg1']).format(ctx.message.author.mention, member.mention),
        str(S_MESSAGE['s_msg2']).format(ctx.message.author.mention, member.mention),
    ]
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- Slap Someone ---",
        description=random.choice(desc),
    )
    embed.set_image(url=imgdata)
    embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

@client.command()
async def bonk(ctx, member : discord.Member=None):
    """Bonk your friends or yourself"""
    if member is None:
        member = ctx.author
    url5 = SFW['bonk1']
    r5 = requests.get(url5)
    data5 = r5.json()
    imgdata = data5['url']
    desc = [
        str(B_MESSAGE['b_msg1']).format(ctx.message.author.mention, member.mention),
        str(B_MESSAGE['b_msg2']).format(ctx.message.author.mention, member.mention),
        str(B_MESSAGE['b_msg3']).format(member.mention),
    ]
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- Bonk!! ---",
        description=random.choice(desc)
    )
    embed.set_image(url=imgdata)
    embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
    await ctx.send(embed=embed)

@client.command()
async def meme(ctx):
    """Random Meme Image"""
    url6 = MEME['meme1']
    r6 = requests.get(url6)
    data6 = r6.json()
    imgdata = data6['url']
    desc = [
        str(M_MESSAGE['m_msg1']).format(ctx.message.author.mention),
        str(M_MESSAGE['m_msg2']).format(ctx.message.author.mention),
        str(M_MESSAGE['m_msg3']).format(ctx.message.author.mention),
        str(M_MESSAGE['m_msg4']).format(ctx.message.author.mention),
    ]
    embed = discord.Embed(
        color=discord.Color.green(),
        title=data6['title'],
        description=random.choice(desc)
    )
    embed.set_image(url=imgdata)
    embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
    
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
    embed.set_footer(text="Author: {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
    
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
    embed.set_footer(text="Author: {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
    
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
    embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

@client.command()
async def showimg(ctx, *, search):
    ran = random.randint[0,9]
    resource = build("customsearch","v1",developerKey=CONFIG['google_api_key']).cse()
    result = resource.list(
        q=f"{search}",
        cx="4891a95939270d95",
        searchType="image"
    ).execute()
    imgdata = result["items"][ran]["link"]
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- Image Search ---",
        description=f"Here your Image ({search.title()})"
    )
    embed.set_image(url=imgdata)
    embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

client.run(CONFIG['token'])
