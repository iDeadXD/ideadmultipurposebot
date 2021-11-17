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
from twilio.rest import Client
from config import CONFIG
from imgapi import SFW, NSFW, MEME
from msg_channel import CHANNEL
from custom_msg import W_MESSAGE, H_MESSAGE, B_MESSAGE, S_MESSAGE, M_MESSAGE
from saved_number import PHONE, USERS, SENDER

client = commands.Bot(command_prefix=CONFIG['prefix'], intents = discord.Intents.all())

cogs = [music]

welcome = f"""I'm Online Right Now.
Author: iDead#9496."""

for i in range(len(cogs)):
    cogs[i].setup(client)

twilioClient = Client(CONFIG['twilio_sid'], CONFIG['twilio_token'])

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
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        
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
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
            
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
    embed.set_footer(text="Requested by {}".format(ctx.message.author.mention), icon_url=ctx.message.author.avatar_url)
    
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
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
        
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
    embed.set_footer(text="Requested by {}".format(ctx.message.author.name), icon_url=ctx.message.author.avatar_url)
    
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

@client.command()
async def localmsg(ctx, member : discord.Member=None):
    """Send message outside Discord"""
    user1 = client.get_user(int(USERS['dafa']))
    user2 = client.get_user(int(USERS['rafi']))
    user3 = client.get_user(int(USERS['wafi']))
    
    if member is None:
        await ctx.send("Note: You must tag someone before send")
        return
    
    try:
        if member is user1:
            twilioClient.messages.create(
                to = int(PHONE['dafa']),
                from_ = int(SENDER['secret']),
                body = "{} - {}".format(ctx.message.author.name, ctx.message.content)
            )
            print("Sent Message: {} - {}".format(ctx.message.author.name, ctx.message.content))
        elif member is user2:
            twilioClient.messages.create(
                to = int(PHONE['rafi']),
                from_ = int(SENDER['secret']),
                body = "{} - {}".format(ctx.message.author.name, ctx.message.content)
            )
            print("Sent Message: {} - {}".format(ctx.message.author.name, ctx.message.content))
        elif member is user3:
            twilioClient.messages.create(
                to = int(PHONE['wafi']),
                from_ = int(SENDER['secret']),
                body = "{} - {}".format(ctx.message.author.name, ctx.message.content)
            )
            print("Sent Message: {} - {}".format(ctx.message.author.name, ctx.message.content))
    except Exception as e:
        await ctx.send("Note: You must verify your(target) number. DM to {} for helping verify target number".format(user2.mention))
        print("Error occured | "+str(e))
    

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
        description=f"{avamem.mention} Profile Avatar",
    )
    embed.set_image(url=useravatar)
    embed.set_footer(text="Requested by {}".format(author), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

client.run(CONFIG['token'])
