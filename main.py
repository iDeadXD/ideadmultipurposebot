import os
import discord
from discord.ext import commands, tasks
from datetime import datetime
from itertools import chain
import random
import psutil
import time
from pymongo import MongoClient
import asyncio
import pytz
import setups
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

#=== Server Blacklist ===
blacklist = []

#=== Prefix Database (MongoDB) ===
cluster = MongoClient(CONFIG['mongodb_url'])

levelling = cluster["database2"]

collection = levelling["prefixes"]

devinfo = cluster['database4']

devage = devinfo['reminder']

dataclient = cluster['database6']

savedch = dataclient['msgchannel']

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
client = commands.Bot(command_prefix=get_prefixes, intents=discord.Intents.all(), case_insensitive=True, owner_ids=[843132313562513408, 695390633505849424], activity=discord.Activity(type=discord.ActivityType.listening, name="<prefix>help"), strip_after_prefix=True)
client.help_command = MyNewHelp()

#=== Cog List ===
cogs = [setups, dev, music, levelsystem, voice_temp, moderation, utils, guild_utils, games, economy]

#=== Cog Executor ===
for i in range(len(cogs)):
    cogs[i].setup(client)

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
    curr_cogs = len(cogs)
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
    print ('[*] Total number of CPUs :' + str(vcc))
    print ('[*] Total CPUs utilized percentage :' + str(vcpu) + '%')
    print('[*] Total Memory = ' + mem_T +' MB')
    print('[*] Used Memory = ' + mem_U +' MB')
    print('[*] Free Memory = ' + mem_F +' MB')

@client.event #on_message
async def on_message(message):
    hello_m = ["halo", "hello", "hola"]
    devmention = [
        "Wait...",
        "Waiting for {} response...",
        "Looks like, {} is busy rn. (Maybe)",
    ]
    
    devoffline = [
        "Maybe {} is offline...",
        "Wait until {} is online",
        "{} is offline rn"
    ]
    
    dev = client.get_guild(message.guild.id).get_member(843132313562513408)
    
    for msg in hello_m: #Check if message content in hello_m
        if message.guild.id == 836464932236165140:
            return
        if message.content.lower().startswith(msg):
            halo = discord.Embed(
                title="",
                description=f"Halo juga {message.author.mention}, Semoga Hari mu Menyenangkan.",
                color=discord.Color.purple()
            )
            await message.reply(embed=halo)
    
    if dev in message.mentions:
        try:
            data = collection.find_one({'guild_id': message.guild.id})
            
            if data is None:
                cmd_prefix = '>'
            else:
                cmd_prefix = data['_prefix']
            
            if message.content.lower().startswith(cmd_prefix):
                return await client.process_commands(message)
            if message.author.bot:
                return
            elif message.author == dev:
                return await message.reply('My Developer.')
            else:
                if dev.status is discord.Status.offline:
                    offmsg = random.choice(devoffline)
                    return await message.reply(offmsg.format(dev.mention))
                
                await client.wait_for('message', check=lambda message:message.author == dev, timeout=180)
        except asyncio.TimeoutError:
            msg = random.choice(devmention)
            return await message.reply(msg.format(dev.mention))
    
    await client.process_commands(message)

@client.event
async def on_member_join(member):
    if member.guild.id == 836464932236165140:
        return
    data = savedch.find_one({'_id': member.guild.id})
    
    if data is None:
        main_ch = member.guild.system_channel
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
        description=error,
        color=discord.Color.red()
    )
    await ctx.send(embed=failed)

@client.event
async def on_guild_join(guild):
    if guild.id in blacklist:
        warn = discord.Embed(
            title='--- Warning!! ---',
            description='Your Server has been Blacklisted!!. Auto Leave Triggered',
            color=discord.Color.red()
        )
        warn.add_field(name='Server Name', value=f'**{guild.name}**')
        warn.add_field(name='Status', value=f'{len(guild.members)} User, {len(guild.roles)} Roles, {len(guild.channels)} Channel')
        warn.add_field(name='\u200b', value='__Blacklisted!!__')
        await guild.owner.send(embed=warn)
        await asyncio.sleep(5)
        return await guild.leave()
    
    dev = client.get_user(843132313562513408)
    owner = guild.owner
    ch = random.choice(guild.text_channels)
    link = await ch.create_invite(xkcd=True, max_age = 0, max_uses = 0)
    
    joined = discord.Embed(
        title='--- Server Joined ---',
        description=f'Joined to **{guild.name}**\nAuthor: __{owner.name + "#" + owner.discriminator}__\nInvite Link: [Click This]({link})',
        color=discord.Color.purple()
    )
    await dev.send(embed=joined)

@client.event
async def on_member_remove(member):
    data = savedch.find_one({'_id': member.guild.id})
    
    if data is None:
        main_ch = member.guild.system_channel
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

#=== Custom Tasks ===
@tasks.loop(minutes=5)
async def dev_hbd():
    now = datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%d/%m, %H:%M:%S")
    devdata = devage.find_one({'devid': 843132313562513408})
    dev = client.get_user(843132313562513408)
    if now == '13/01, 00:00:00':
        age_now = devdata['age'] + 1
        devage.update_one({'devid': 843132313562513408}, {'$set': {'age': age_now}})
        congrats = discord.Embed(
            title='--- Announcement ---',
            description=f'Dev ({dev.name + "#" + dev.discriminator}): Today is my birthday. My current age is {str(age_now)} years old.\nHopefully I can be better at developing this bot.\n(This message is sent automatically)',
            color=discord.Color.purple()
        )
        print(f"Happy Birthday, {dev.name + '#' + dev.discriminator}")
        await client.guilds.system_channel.send(embed=congrats)

@dev_hbd.before_loop
async def dev_hbd_before():
    await client.wait_until_ready()

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

#=== Tasks Runner ===
dev_hbd.start()

#=== Client Account Executor ===
print('[*] Creating Connection to Discord...')
time.sleep(5)
print('[*] Authenticating Connection...')
time.sleep(4)
print('[*] Connecting to Discord...')
time.sleep(5)
print('[*] Connected to Discord!')
time.sleep(0.5)
print('[*] Running...')
time.sleep(2)
print('[*] ----------------')
client.run(os.environ.get('TOKEN'))
