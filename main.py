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
import pymongo
from pymongo import MongoClient
from config import CONFIG
from imgapi import SFW, NSFW, MEME, WELCOME
from msg_channel import CHANNEL
from custom_msg import W_MESSAGE, H_MESSAGE, B_MESSAGE, S_MESSAGE, M_MESSAGE, K_MESSAGE, J_MESSAGE

client = commands.Bot(command_prefix=[CONFIG['prefix1'], CONFIG['prefix2']], intents = discord.Intents.all())

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

@client.event
async def on_message(ctx):
    mango_url = "mongodb+srv://idead:idead@botdb.kqqpj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority_id"
    cluster = MongoClient(mango_url)
    db = cluster["databasel"]
    collection = db["level"]
    author_id = ctx.author.id
    guild_id = ctx.guild.id 
    
    author = ctx.author
    
    user_id = {"_id": author_id}
    
    if ctx.author == client.user:
        return
    
    if ctx.author.bot:
        return
    
    if(collection.count_documents({}) == 0):
        user_info = {"_id": author_id, "GuildID": guild_id, "Level": 1, "XP": 0}
        collection.insert_one(user_info)
    
    if(collection.count_documents(user_id) == 0):
        user_info = {"_id": author_id, "GuildID": guild_id, "Level": 1, "XP": 0}
        collection.insert_one(user_info)
    
    exp = collection.find(user_id)
    for xp in exp:
        cur_xp = xp["XP"]
    
        new_xp = cur_xp + 1 
    
    collection.update_one({"_id": author_id}, {"$set":{"XP":new_xp}}, upsert=True)
    
    #await ctx.channel.send("1 xp up")
  
    lvl = collection.find(user_id)
    for levl in lvl:
        lvl_start = levl["Level"]
    
        new_level = lvl_start + 1
    
    if cur_xp >= round(5 * (lvl_start ** 4 / 5)):
        collection.update_one({"_id": author_id}, {"$set":{"Level":new_level}}, upsert=True)
        await ctx.channel.send(f"{author.name} has leveled up to {new_level}!")

@client.command()
async def waifu(ctx, member : discord.Member=None):
    """Waifu Image for You"""
    if member is None:
        member = ctx.author
    if ctx.channel.is_nsfw():
        await ctx.send('Note: Write this command outside the NSFW channel')
        await ctx.message.delete()
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
    sleeper=5
    await asyncio.sleep(sleeper)
    await ctx.message.delete()

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
        sleeper=5
        await asyncio.sleep(sleeper)
        await ctx.message.delete()
    else:
        await ctx.send('Note: Write this command in NSFW channel')
        sleeper=5
        await asyncio.sleep(sleeper)
        await ctx.message.delete()

@client.command()
async def kiss(ctx, member : discord.Member=None):
    if member is None:
        await ctx.send("Note: No G*Y/Selfkiss!!! You must tag someone for your kiss partner")
        await ctx.message.delete()
        return
    url7 = SFW['kiss1']
    r7 = requests.get(url7)
    data7 = r7.json()
    imgdata = data7['url']
    desc = [
        str(K_MESSAGE['k_msg1']).format(ctx.message.author.mention, member.mention),
        str(K_MESSAGE['k_msg2']).format(ctx.message.author.mention, member.mention),
    ]
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- Kiss for You ---",
        description=random.choice(desc)
    )
        
    embed.set_image(url=imgdata)
    embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
    await ctx.send(embed=embed)
    sleeper=5
    await asyncio.sleep(sleeper)
    await ctx.message.delete()

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
    sleeper=5
    await asyncio.sleep(sleeper)
    await ctx.message.delete()

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
    sleeper=5
    await asyncio.sleep(sleeper)
    await ctx.message.delete()

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
    sleeper=5
    await asyncio.sleep(sleeper)
    await ctx.message.delete()

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

@client.command(name="clean")
async def clean_(ctx, amount=100):
    await ctx.channel.purge(limit=amount)
    done = await ctx.send("👍")
    await asyncio.sleep(6)
    await done.delete()

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
async def serverinfo(ctx):
    member = ctx.guild.owner
    role_count = len(ctx.guild.roles)
    list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
        
    embed2 = discord.Embed(timestamp=ctx.message.created_at, color=ctx.author.color)
    embed2.add_field(name='Name', value=f"{ctx.guild.name}", inline=False)
    embed2.add_field(name='Owner', value=f"{member.mention}", inline=False)
    embed2.add_field(name='Verification Level', value=str(ctx.guild.verification_level), inline=False)
    embed2.add_field(name='Highest role', value=ctx.guild.roles[-2], inline=False)
        
    embed2.add_field(name='Number of roles', value=str(role_count), inline=False)
    embed2.add_field(name='Number Of Members', value=ctx.guild.member_count, inline=False)
    embed2.add_field(name='Bots:', value=(', '.join(list_of_bots)))
    embed2.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
    embed2.set_thumbnail(url=ctx.guild.icon_url)
    embed2.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
    await ctx.send(embed=embed2)

@client.command()
async def botinfo(ctx):
    botdev = client.get_user(843132313562513408)
    embed = discord.Embed(
        color=ctx.author.color,
        title="--- Bot Information ---"
    )
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="Bot Name", value=f"{client.user.mention}", inline=False)
    embed.add_field(name="Real Bot Name", value="Music Player.py#6361", inline=False)
    embed.add_field(name="Bot Author", value=f"{botdev.mention}", inline=False)
    embed.add_field(name='Created At', value=client.user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
    embed.add_field(name="Coded in", value="Python3 (discord.py Module)", inline=False)
    embed.add_field(name="Bot Category", value="Music Bot (Soon, this bot will be a MultiPurpose bot)", inline=False)
    embed.add_field(name="Auxiliaries", value="Heroku Server (So that bots can always be online)", inline=False)
    embed.add_field(name="Available Commands", value="Check using >help or .help", inline=False)
    embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
    
    await ctx.send(embed=embed)

@client.command()
async def ban(ctx, member : discord.Member=None, *, reason=None):
    if ctx.message.author is not ctx.guild.owner:
        await ctx.send("You're not Owner in this Server. Command Ignored")
        return
    if reason is None:
        await ctx.send("Reason required!!")
        return
    if member is ctx.guild.owner and member != None:
        await ctx.send("Owner!!. You can't ban Server Owner")
        return
    if member is None:
        await ctx.send("You have to choose a member to get banned. Command Ignored")
        return
    else:
        guild = ctx.guild.name
        await member.ban()
        embed = discord.Embed(
            title="--- Banned Member ---",
            color=discord.Color.red()
        )
        embed.add_field(name="Member Name", value=f"{member.mention}")
        embed.add_field(name="Punishment", value="Banned from Server")
        embed.add_field(name="Reason", value=f"{reason}")
        embed.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
        embed.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")))
        
        banned = discord.Embed(
            title="--- You have been Banned ---",
            color=discord.Color.red()
        )
        banned.add_field(name="Punishment", value="Banned from Server")
        banned.add_field(name="Reason", value=f"{reason}")
        banned.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
        banned.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")))
        
        await ctx.send(embed=embed)
        await ctx.send("✔ User has been notified.")
        await member.send(embed=banned)

@client.command()
async def kick(ctx, member : discord.Member=None, *, reason=None):
    if ctx.message.author is not ctx.guild.owner:
        await ctx.send("You're not Owner in this Server. Command Ignored")
        return
    if reason is None:
        await ctx.send("Reason required!!")
        return
    if member is ctx.guild.owner and member != None:
        await ctx.send("Owner!!. You can't kick Server Owner")
        return
    else:
        guild = ctx.guild.name
        await member.kick()
        embed = discord.Embed(
            title="--- Kicked Member ---",
            color=discord.Color.red()
        )
        embed.add_field(name="Member Name", value=f"{member.mention}")
        embed.add_field(name="Punishment", value="Kicked from Server")
        embed.add_field(name="Reason", value=f"{reason}")
        embed.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
        embed.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")))
        
        kicked = discord.Embed(
            title="--- You have been Kicked ---",
            color=discord.Color.red()
        )
        kicked.add_field(name="Punishment", value="Kicked from Server")
        kicked.add_field(name="Reason", value=f"{reason}")
        kicked.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
        kicked.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")))
        
        await ctx.send(embed=embed)
        await ctx.send("✔ User has been notified.")
        await member.send(embed=kicked)

@client.command()
async def userinfo(ctx, member: discord.Member=None):
    if member is None:
        member = ctx.author
    
    rolelist = [role.mention for role in member.roles if role.mentionable]
    text = "Nothing was found..." if len(rolelist) == 0 else ', '.join(rolelist)
    
    embed = discord.Embed(
        color=discord.Color.magenta(),
        title="--- User Information ---"
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name="ID", value=f"{member.id}")
    embed.add_field(name="Nickname", value=f"{member.display_name}")
    embed.add_field(name="Current Status", value=f"{member.status}")
    embed.add_field(name="Mention", value=f"{member.mention}")
    embed.add_field(name="Joined at", value=f"{member.joined_at.__format__('%A, %d. %B %Y @ %H:%M:%S')} UTC")
    embed.add_field(name="User Roles", value=text)
    embed.set_footer(text=f"Created at {member.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')} UTC")
    
    await ctx.send(embed=embed)

@client.command()
async def sendto(ctx, member : discord.Member=None, *, arg=None):
    if member is None or member is ctx.message.author:
        await ctx.send("You can't send DM to yourself")
        return
    if arg is None:
        await ctx.send("Please, write your message")
        return
    else:
        embed = discord.Embed(
            color=discord.Color.purple(),
            title="--- Someone DM You ---",
            description=f"From {ctx.message.author.mention} to {member.mention}"
        )
        embed.set_thumbnail(url=ctx.message.author.avatar_url)
        embed.add_field(name="This is the message", value=arg)
        embed.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")))

        
        embed1 = discord.Embed(
            color=discord.Color.green()
        )
        embed1.set_thumbnail(url=member.avatar_url)
        embed1.add_field(name=f"✔ The message has been sent.", value=f"Sent to: {member.mention}")
        embed1.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")))
        
        await ctx.message.delete()
        await ctx.send(embed=embed1)
        await asyncio.sleep(5)
        await member.send(embed=embed)

@client.command()
async def invite(ctx, *, uses=None):
    guild = ctx.guild.name
    if uses is None:
        await ctx.send("Insert Max Used value (0 for Unlimited Use). Example: >invite 5(Limit Link can Used: 5Times/5User)")
        return
    link = await ctx.channel.create_invite(xkcd=True, max_age = 0, max_uses = int(uses))
    embed = discord.Embed(
        color=discord.Color.purple(),
        title="--- Instant Invite Link ---",
        description="Share this invite link to another user"
    )
    embed.add_field(name="This invite link will be directed to: ", value=guild)
    embed.add_field(name="Max Uses", value=uses)
    embed.add_field(name="This your invite link", value=f"[Hold for Copy the link]({link})")
    
    await ctx.message.delete()
    await ctx.send(embed=embed)

@client.command()
async def invitebot(ctx):
    link = "https://discord.com/api/oauth2/authorize?client_id=904156026851455006&permissions=433103232119&scope=bot%20applications.commands"
    embed = discord.Embed(
        color=discord.Color.green(),
        title="--- Invite Link ---"
    )
    embed.set_thumbnail(url=client.user.avatar_url)
    embed.add_field(name="Click the link below to invite me to your server!", value=f"[Invite Me!]({link})")
    
    await ctx.send(embed=embed)

client.run(CONFIG['token'])
