import os
import discord
from discord.ext import commands
from datetime import datetime
from pymongo import MongoClient
import pytz
import music
import levelsystem
import voice_temp
import guild_utils
import moderation
import utils
from config import CONFIG
from guild_utils import Guilds
from msg_channel import CHANNEL

#=== Prefix Database (MongoDB) ===
cluster = MongoClient("mongodb+srv://idead:idead@botdb.kqqpj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")

levelling = cluster["database2"]

collection = levelling["prefixes"]

#=== Client Prefix Setup ===

async def get_prefixes(client, message):
    global cluster
    default_prfx = ">"
    
    if not message.guild:
        return commands.when_mentioned_or(default_prfx)(client, message)
    
    db = cluster.bot
    posts = db.server
    
    for x in posts.find({"guild_id": message.guild.id}):
        prfxs = x["_prefix"]
    return commands.when_mentioned_or(prfxs)(client, message)

#=== Client Setup ===
client = commands.Bot(command_prefix=get_prefixes, intents = discord.Intents.all())

#=== Cog List ===
cogs = [music]
cogs2 = [levelsystem]
cogs3 = [voice_temp]
cogs4 = [moderation]
cogs5 = [utils]
cogs6 = [guild_utils]

#=== Welcome Messages ===
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

for i in range(len(cogs6)):
    cogs6[i].setup(client)

#=== Client Event Executor ===
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
async def on_member_join(member):
    main_ch = member.guild.system_channel
    
    welcome = discord.Embed(
        title="--- New Member Joined ---",
        description=f"Welcome to {member.guild.name}!!",
        color=discord.Color.purple()
    )
    welcome.set_thumbnail(url=member.avatar_url)
    welcome.add_field(name="Member name", value=f"{member.mention}")
    welcome.add_field(name="Joined at", value="Today, {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%H:%M:%S')))
    
    await main_ch.send(embed=welcome)

@client.event
async def on_member_remove(member):
    main_ch = member.guild.system_channel
    
    leave = discord.Embed(
        title="--- Member Leave a Server ---",
        description=f"Someone leave from {member.guild.name}!!",
        color=discord.Color.red()
    )
    leave.set_thumbnail(url=member.avatar_url)
    leave.add_field(name="Member name", value=f"{member.mention}")
    leave.add_field(name="Leaved at", value="Today, {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%H:%M:%S')))
    
    await main_ch.send(embed=leave)

#=== Prefix Commands ===
@client.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, prefixs=None):
    """Change bot command prefix"""
    if prefixs is None:
        fail =discord.Embed(
            title="",
            description="Enter your prefix to change the default prefix. Default Prefix: >",
            color=discord.Color.green()
        )
        fail.set_thumbnail(url=client.user.avatar_url)
        
        return await ctx.send(embed=fail)
    
    data = collection.find_one({"guild_id": ctx.guild.id})
    if data is None:
        newdata = {"guild_id": ctx.guild.id, "_prefix": prefixs}
        collection.insert_one(newdata)
    else:
        collection.update_one({"guild_id": ctx.guild.id}, {"$set": {"_prefix": prefixs}}, upsert=True)
    
    done = discord.Embed(
        title="",
        description=f"{client.user.mention}'s Prefix has been set to {prefixs}",
        color=discord.Color.green()
    )
    done.set_thumbnail(url=client.user.avatar_url)
    
    await ctx.send(embed=done)
    
@client.command()
@commands.has_permissions(manage_guild=True)
async def deleteprefix(ctx):
    """Set changed prefix to default prefix"""
    collection.update_one({"guild_id": ctx.guild.id}, {"$unset": {"_prefix": 1}})
    
    done = discord.Embed(
        title="",
        description=f"{client.user.mention}'s Prefix has been set to default ( > )",
        color=discord.Color.green()
    )
    done.set_thumbnail(url=client.user.avatar_url)
    
    await ctx.send(embed=done)

#=== Client Account Executor ===
client.run(CONFIG['token'])
