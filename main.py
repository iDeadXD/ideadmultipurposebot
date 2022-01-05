import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from itertools import chain
import psutil
import time
from pymongo import MongoClient
import pytz
import music
import levelsystem
import voice_temp
import guild_utils
import economy
import dev
import moderation
import utils
import games
from config import CONFIG
from guild_utils import Guilds
from msg_channel import CHANNEL

#=== Prefix Database (MongoDB) ===
cluster = MongoClient(CONFIG['mongodb_url'])

levelling = cluster["database2"]

collection = levelling["prefixes"]

#=== Client Prefix Setup ===
async def get_prefixes(client, message):
    
    if not message.guild:
        return commands.when_mentioned_or(">")(client, message)
    
    default_prfx = ">"
    
    for x in collection.find({"guild_id": message.guild.id}):
        default_prfx = x["_prefix"]
    return commands.when_mentioned_or(str(default_prfx))(client, message)

#=== Custom Help Command ===
class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=discord.Color.purple())
            emby.set_thumbnail(url=client.user.avatar_url)
            await destination.send(embed=emby)
    
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color=discord.Color.purple())
        embed.add_field(name="Help", value=command.help)
        alias = command.aliases
        if alias:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error, color=discord.Color.red())
        channel = self.get_destination()
        await channel.send(embed=embed)

#=== Client Setup ===
client = commands.Bot(command_prefix=get_prefixes, intents=discord.Intents.all(), case_insensitive=True, owner_id=843132313562513408, activity=discord.Activity(type=discord.ActivityType.listening, name="<prefix>help"))
client.help_command = MyNewHelp()

#=== Cog List ===
cogs = [music]
cogs2 = [levelsystem]
cogs3 = [voice_temp]
cogs4 = [moderation]
cogs5 = [utils]
cogs6 = [guild_utils]
cogs7 = [games]
cogs8 = [economy]
cogs9 = [dev]
printcogs = [dev, music, levelsystem, voice_temp, moderation, utils, guild_utils, games, economy]

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

for i in range(len(cogs7)):
    cogs7[i].setup(client)

for i in range(len(cogs8)):
    cogs8[i].setup(client)

for i in range(len(cogs9)):
    cogs9[i].setup(client)

#=== Client Event Executor ===
@client.event #bot_event
async def on_ready():
    #=== Memory Indentifier ===
    mem=str(os.popen('free -t -m').readlines())
    T_ind=mem.index('T')
    mem_G=mem[T_ind+14:-4]
    S1_ind=mem_G.index(' ')
    mem_T=mem_G[0:S1_ind]
    mem_G1=mem_G[S1_ind+8:]
    S2_ind=mem_G1.index(' ')
    mem_U=mem_G1[0:S2_ind]
    mem_F=mem_G1[S2_ind+8:]
    
    #=== CPU Indentifier ===
    vcc=psutil.cpu_count()
    vcpu=psutil.cpu_percent()
    
    #=== Client Indicator ===
    curr_cogs = len(printcogs)
    curr_server = len(client.guilds)
    print('[*] BOT: Online')
    time.sleep(0.8)
    print(f'[*] Username: {client.user}')
    print(f'[*] ID: {str(client.user.id)}')
    print(f'[*] Ping: {str(round(client.latency * 1000))}ms')
    time.sleep(0.8)
    print(f'[*] Loaded Cogs: {curr_cogs}')
    print(f'[*] Serving on: {curr_server} Server')
    time.sleep(0.8)
    print('[*] --- System Information ---')
    print ('[*] Total number of CPUs :' + vcc)
    print ('[*] Total CPUs utilized percentage :' + vcpu + '%')
    print('[*] Total Memory = ' + mem_T +' MB')
    print('[*] Used Memory = ' + mem_U +' MB')
    print('[*] Free Memory = ' + mem_F +' MB')

@client.event #on_message
async def on_message(message):
    hello_m = ["halo", "hello", "hola"]
    
    for msg in hello_m: #Check if message content in hello_m
        if message.content.lower().startswith(str(msg)):
            halo = discord.Embed(
                title="",
                description=f"Halo juga {message.author.mention}, Semoga Hari mu Menyenangkan.",
                color=discord.Color.purple()
            )
            await message.reply(embed=halo)
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    main_ch = member.guild.system_channel
    
    welcome = discord.Embed(
        title="--- New Member Joined ---",
        description=f"Welcome to {member.guild.name}!!",
        color=discord.Color.purple()
    )
    welcome.set_thumbnail(url=member.avatar_url)
    welcome.add_field(name="Member name", value=f"{member.name + '#' + member.discriminator}")
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
    leave.add_field(name="Member name", value=f"{member.name + '#' + member.discriminator}")
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
            description=f"Enter your prefix to change the current prefix.",
            color=discord.Color.green()
        )
        fail.set_thumbnail(url=client.user.avatar_url)
        
        return await ctx.send(embed=fail)
    
    data = collection.find_one({"guild_id": ctx.guild.id})
    if data is None:
        newdata = {"guild_id": ctx.guild.id, "_prefix": prefixs}
        collection.insert_one(newdata)
    
    collection.update_one({"guild_id": ctx.guild.id}, {"$set": {"_prefix": prefixs}}, upsert=True)
    
    done = discord.Embed(
        title="",
        description=f"{client.user.mention}'s Prefix has been set to {prefixs}",
        color=discord.Color.green()
    )
    done.set_thumbnail(url=client.user.avatar_url)
    
    await client.get_guild(ctx.guild.id).get_member(client.user.id).edit(nick=f"Music Player [{str(prefixs)}]")
    await ctx.send(embed=done)

@client.command()
@commands.has_permissions(manage_guild=True)
async def deleteprefix(ctx):
    """Set changed prefix to default prefix"""
    defaults = ">"
    collection.update_one({"guild_id": ctx.guild.id}, {"$set": {"_prefix": defaults}})
    
    done = discord.Embed(
        title="",
        description=f"{client.user.mention}'s Prefix has been set to default ( > )",
        color=discord.Color.green()
    )
    done.set_thumbnail(url=client.user.avatar_url)
    
    await client.get_guild(ctx.guild.id).get_member(client.user.id).edit(nick=f"Music Player [{str(defaults)}]")
    await ctx.send(embed=done)

@client.command(hidden=True)
async def donate(ctx):
    link = "https://youtu.be/dQw4w9WgXcQ"
    embed = discord.Embed(
        title="--- Donate Me ---",
        description="Donate me for support this project!!",
        color=discord.Color.green()
    )
    embed.add_field(name="Saweria", value=f"[Saweria Link]({link})")
    await ctx.send(embed=embed)

#=== Client Account Executor ===
client.run(os.environ.get('TOKEN'))
