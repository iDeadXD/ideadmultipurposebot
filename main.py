import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from itertools import chain
import re
import random
import psutil
import time
import pymongo
from pymongo import MongoClient
import asyncio
import logging
import sys
import pytz
import setups
import music
import levelsystem
import voice
import guild_utils
import economy
import dev
import moderation
import utils
import premium
from menupages import MyMenuPages
from helpsource import HelpPageSource
from config import CONFIG
from guild_utils import Guilds
from msg_channel import CHANNEL

#=== Server Whitelist ===
whitelist = [785349273242959883, 948593220324057129, 840594344939356181, 851745883825373225, 919177496669351956, 939164890705297418]

#=== Prefix Database (MongoDB) ===
cluster = MongoClient(CONFIG['mongodb_url'])

levelling = cluster["database2"]

collection = levelling["prefixes"]

devinfo = cluster['database4']

devage = devinfo['reminder']

dataclient = cluster['database6']

savedch = dataclient['msgchannel']

#=== Logging Stream -> Console ===
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

#=== Saved Phising List ===
with open('phising_list.txt') as phising_list:
    phising_domain = phising_list.read().splitlines()

#=== Client Prefix Setup ===
async def get_prefixes(client, message):
    
    if not message.guild:
        return commands.when_mentioned_or(">")(client, message)
    
    default_prfx = ">"
    
    for x in collection.find({"guild_id": message.guild.id}):
        default_prfx = x["_prefix"]
    return commands.when_mentioned_or(str(default_prfx))(client, message)

#=== Custom Error Class ===
class ErrorHandler(commands.CommandError):
    pass

#=== Custom Help Command ===
class MyNewHelpv1(commands.MinimalHelpCommand):
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

class MyNewHelpv2(commands.MinimalHelpCommand):
    def get_command_brief(self, command):
        return command.short_doc or "Command is not documented."
    
    async def send_bot_help(self, mapping):
        all_commands = list(chain.from_iterable(mapping.values()))
        formatter = HelpPageSource(all_commands, self)
        menu = MyMenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)
    
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

#=== RPC Timestamp Setup ===
presentDate = datetime.now(pytz.timezone('Asia/Jakarta')) 
unix_timestamp = datetime.timestamp(presentDate)*1000

#=== Client Setup ===
client = commands.Bot(
    command_prefix=get_prefixes,
    intents=discord.Intents.all(),
    case_insensitive=True,
    strip_after_prefix=True,
    owner_ids=[843132313562513408, 695390633505849424],
    activity=discord.Activity(type=discord.ActivityType.listening, name='<prefix>help'),
)
client.help_command = MyNewHelpv1()

#=== Cog + Task List ===
#cogs = [voice, setups, dev, music, levelsystem, moderation, utils, guild_utils, games, economy]
task = ['good_morning']

#=== Cog Executor ===
#for i in range(len(cogs)):
#    cogs[i].setup(client)

#=== Client Event Executor ===
@client.event #bot_event
async def on_ready():
    #=== Memory Indentifier ===
    vmem=psutil.virtual_memory().percent
    
    #=== CPU Indentifier ===
    vcc=psutil.cpu_count()
    vcpu=psutil.cpu_percent()
    
    #=== Client System Indicator ===
    curr_cogs = len(cogs)
    curr_looptask = len(task)
    curr_server = len(client.guilds)
    
    logger.info('[*] BOT: Online')
    time.sleep(0.8)
    logger.info(f'[*] Username: {client.user}')
    logger.info(f'[*] ID: {str(client.user.id)}')
    logger.info(f'[*] Latency: {str(round(client.latency * 1000))}ms')
    time.sleep(0.8)
    logger.info(f'[*] Loaded Cogs: {curr_cogs}')
    logger.info(f'[*] Serving on: {curr_server} Server')
    logger.info(f'[*] {curr_looptask} Loop Tasks Started.')
    time.sleep(0.8)
    logger.info('[*] --- Advance Information ---')
    logger.info('[*] Total number of CPUs :' + str(vcc))
    logger.info('[*] Total CPUs utilized percentage :' + str(vcpu) + '%')
    logger.info('[*] Memory usage percentage :' + str(vmem) + '%')
    logger.info('[*] Discord.py Version: ' + discord.__version__)
    logger.info('[*] PyMongo Version: ' + pymongo.version)

@client.event #on_message
async def on_message(message):
    #hello_m = ["halo", "hello", "hola"]
    #test_msg = ['kntl_is_kntl', 'mmk_is_mmk']
    
    #for msg in hello_m: Check if message content in hello_m
        #if message.content.lower().startswith(msg):
            #halo = discord.Embed(
                #title="",
                #description=f"Halo juga {message.author.mention}, Semoga Hari mu Menyenangkan.",
                #color=discord.Color.purple()
            #)
            #await message.reply(embed=halo)
    
    if message.channel.id == 906005326086692904:
        if message.attachments:
            emoji_list = ['👌', '👍', '💯', '❤️']
            await message.add_reaction(random.choice(emoji_list))
    
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    data = savedch.find_one({'_id': member.guild.id})
    
    if data is None:
        return
    else:
        main_ch = client.get_channel(data['welcome_ch'])
    
    welcome = discord.Embed(
        title="--- New Member Joined ---",
        description=f"Welcome to {member.guild.name}!!",
        color=discord.Color.purple()
    )
    welcome.set_thumbnail(url=member.avatar_url)
    welcome.add_field(name="Member name", value=f"{member.name + '#' + member.discriminator}")
    welcome.add_field(name="Joined at", value="{}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%A, %d/%m/%Y, %H:%M:%S')))
    
    await main_ch.send(embed=welcome)

@client.event
async def on_command_error(ctx, error):
    failed = discord.Embed(
        title='Error',
        description=f'`{error}`',
        color=discord.Color.red()
    )
    await ctx.message.delete()
    await ctx.send(embed=failed, delete_after=5)
    raise error

@client.event
async def on_guild_join(guild):
    dev = client.get_user(843132313562513408)
    #if guild.id not in whitelist:
        #blacklist_owner = guild.owner
        #date_now = datetime.now(pytz.timezone('Asia/Jakarta'))
        #warn = discord.Embed(
            #title='--- Warning!! ---',
            #description='Your Server is not registered!!. Auto Leave Triggered\nYou can request to Dev for registering your Server and invite me again after registration\nReason: BETA Version (Still Under Development)',
            #color=discord.Color.red()
        #)
        #warn.add_field(name='Server Name', value=f'**{guild.name}**')
        #warn.add_field(name='Status', value=f'{len(guild.members)} User, {len(guild.roles)} Roles, {len(guild.channels)} Channel')
        #warn.add_field(name='\u200b', value='__Not Registered!!__')
        
        #blacklist_join = discord.Embed(
            #title='--- Server is not registered ---',
            #description=f'Joined to **{guild.name}**\nAuthor: __{blacklist_owner.name + "#" + blacklist_owner.discriminator}__\nTime: {date_now}',
            #color=discord.Color.red()
        #)
        #blacklist_join.add_field(name='Server Name', value=f'**{guild.name}**')
        #blacklist_join.add_field(name='Status', value=f'{len(guild.members)} User, {len(guild.roles)} Roles, {len(guild.channels)} Channel')
        #blacklist_join.set_footer(text='Unregistered server try to invite me!!')
        
        #await dev.send(embed=blacklist_join)
        #await guild.owner.send(embed=warn)
        #await asyncio.sleep(10)
        #return await guild.leave()
    
    owner = guild.owner
    #ch = random.choice(guild.text_channels)
    #link = await ch.create_invite(xkcd=True, max_age = 0, max_uses = 0)
    
    joined = discord.Embed(
        title='--- Server Joined ---',
        description=f'Joined to **{guild.name}**\nAuthor: __{owner.name + "#" + owner.discriminator}__\nTime: {date_now}',
        color=discord.Color.purple()
    )
    await dev.send(embed=joined)

@client.event
async def on_member_remove(member):
    data = savedch.find_one({'_id': member.guild.id})
    
    if data is None:
        return
    else:
        main_ch = client.get_channel(data['leave_ch'])
    
    leave = discord.Embed(
        title="--- Member Leave a Server ---",
        description=f"Someone leave from {member.guild.name}!!",
        color=discord.Color.red()
    )
    leave.set_thumbnail(url=member.avatar_url)
    leave.add_field(name="Member name", value=f"{member.name + '#' + member.discriminator}")
    leave.add_field(name="Leaved at", value="{}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime('%A, %d/%m/%Y, %H:%M:%S')))
    
    await main_ch.send(embed=leave)

#=== Prefix Commands ===
@client.command()
@commands.has_permissions(manage_guild=True)
async def prefix(ctx, prefix=None):
    """Change bot command prefix"""
    data = collection.find_one({"guild_id": ctx.guild.id})
    curr_prefix = '>' if data is None else data['_prefix']
    
    if prefix is None:
        fail =discord.Embed(
            title="",
            description=f"Enter your prefix to change the current prefix.\nMy Current Prefix: {curr_prefix}",
            color=discord.Color.green()
        )
        fail.set_thumbnail(url=client.user.avatar_url)
        
        return await ctx.send(embed=fail)
    
    if data is None:
        newdata = {"guild_id": ctx.guild.id, "_prefix": prefix}
        collection.insert_one(newdata)
    
    collection.update_one({"guild_id": ctx.guild.id}, {"$set": {"_prefix": prefix}}, upsert=True)
    
    done = discord.Embed(
        title="",
        description=f"{client.user.mention}'s Prefix has been set to {prefix}",
        color=discord.Color.green()
    )
    done.set_thumbnail(url=client.user.avatar_url)
    
    await client.get_guild(ctx.guild.id).get_member(client.user.id).edit(nick=f"Music Player [{str(prefix)}]")
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

@client.command(aliases=['gm'], hidden=True)
@commands.is_owner()
async def good_morning(ctx, channel_id: int=None):
    if channel_id is None:
        return
    channel = client.get_channel(int(channel_id))
    await channel.send(file=discord.File('ohayou.jpg'))
    await ctx.send('Done!')

@client.command()
@commands.is_owner()
async def load_music(ctx):
    await music.setup(cliient)
    await ctx.send("Music Loaded")

@client.command(hidden=True)
@commands.is_owner()
async def rpctest(ctx):
    await client.change_presence(
        activity=discord.Activity(
            application_id=904156026851455006,
            type=discord.ActivityType.playing,
            name=f"Logged in: {client.user}",
            state=f'Serving on {len(client.guilds)} |  <prefix>help',
            details=f'Author: iDead#9496'
        )
    )
    await ctx.send('Done!', delete_after=5)

#=== Client Account Executor ===
if __name__ == "__main__":
    logger.info('[*] Creating Connection to Discord...')
    time.sleep(5)
    logger.info('[*] Authenticating Connection...')
    time.sleep(4)
    logger.info('[*] Connecting to Discord...')
    time.sleep(5)
    logger.info('[*] Connected to Discord!')
    time.sleep(0.5)
    logger.info('[*] Running...')
    time.sleep(2)
    logger.info('[*] ----------------')
    client.run(os.environ.get('TOKEN'))
