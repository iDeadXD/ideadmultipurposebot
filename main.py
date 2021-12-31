import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from itertools import chain
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
client = commands.Bot(command_prefix=get_prefixes, intents=discord.Intents.all(), case_insensitive=True, owner_id=843132313562513408, activity=discord.Activity(type=discord.ActivityType.listening, name=">help"))
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

@client.event
async def on_message(message):
    hello_m = ["halo", "hello", "hola"]
    
    for msg in hello_m:
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
    
    await ctx.send(embed=done)

#=== Custom Tasks ===
@tasks.loop(minutes=1)
async def newyear():
    botdev = client.get_user(843132313562513408)
    check = datetime.now()
    if check.strftime("%d/%m, %H:%M:%S") == "01/01, 00:00:00":
        for guild in client.guilds:
            congrats = discord.Embed(
                title="--- HAPPY NEW YEAR ---",
                description=f"Hopefully this year, everything will be better than before (And hopefully this bot project will be more updated).\nDev, __{botdev.name + '#' + botdev.discriminator}__",
                color=discord.Color.purple()
            )
            print(check.strftime("%d/%m, %H:%M:%S"))
            await guild.system_channel.send(embed=congrats)

@newyear.before_loop
async def newyear_before():
    await client.wait_until_ready()

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

#=== Tasks Executor ===
newyear.start()

#=== Client Account Executor ===
client.run(CONFIG['token'])
