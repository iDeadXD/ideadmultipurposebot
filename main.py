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
import economy
import moderation
import utils
import games
from config import CONFIG
from guild_utils import Guilds
from msg_channel import CHANNEL
from helpsource import HelpPageSource
from menupages import MyMenuPages

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
    def get_command_brief(self, command):
        return command.short_doc or "Command is not documented."
    
    async def send_bot_help(self, mapping):
        all_commands = list(chain.from_iterable(mapping.values()))
        formatter = HelpPageSource(all_commands, self)
        menu = MyMenuPages(formatter, delete_message_after=True)
        await menu.start(self.context)
    
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error)
        channel = self.get_destination()
        await channel.send(embed=embed)

#=== Client Setup ===
client = commands.Bot(command_prefix=get_prefixes, intents = discord.Intents.all(), case_insensitive=True)
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

for i in range(len(cogs7)):
    cogs7[i].setup(client)

for i in range(len(cogs8)):
    cogs8[i].setup(client)

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

#=== Custom Help Commands ===
@client.command(name="_help")
async def _help(ctx, sub: str=None):
    list1 = [c.name for c in cogs.get_commands()] #Music
    list2 = [c.name for c in cogs2.get_commands()] #LevelSystem
    list3 = [c.name for c in cogs3.get_commands()] #VoiceTemp
    list4 = [c.name for c in cogs4.get_commands()] #Moderation
    list5 = [c.name for c in cogs5.get_commands()] #Utils
    list6 = [c.name for c in cogs6.get_commands()] #Guilds
    list7 = [c.name for c in client.commands]
    
    args1 = ["Music", "music"]
    args2 = ["LevelSystem", "Levelsystem", "levelsystem"]
    args3 = ["VoiceTemp", "Voicetemp", "voicetemp"]
    args4 = ["Moderation", "moderation"]
    args5 = ["Utils", "utils"]
    args6 = ["Guilds", "guilds"]
    
    if str(sub) is None:
        default = discord.Embed(
            title="--- List of Bot Help ---",
            color=discord.Color.purple()
        )
        default.set_thumbnail(url=client.user.avatar_url)
        default.add_field(name="**Music**", value=str("```" + ", ".join(list1) + "```"))
        default.add_field(name="**LevelSystem**", value=str("```" + ", ".join(list2) + "```"))
        default.add_field(name="**VoiceTemp**", value=str("```" + ", ".join(list3) + "```"))
        default.add_field(name="**Moderation**", value=str("```" + ", ".join(list4) + "```"))
        default.add_field(name="**Utils**", value=str("```" + ", ".join(list5) + "```"))
        default.add_field(name="**Guilds**", value=str("```", "".join(list6) + "```"))
        default.add_field(name="**No Category", value=str("```" + ", ".join(list7) + "```"))
        default.add_field(name="Another Options", value="You can use ```<your prefix>help separate``` for separate commands list.")
        default.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=default)
    
    if str(sub) == "separate":
        choose = discord.Embed(
            title="--- List of Bot Help ---",
            description="Write one of the command categories below",
            color=discord.Color.purple()
        )
        choose.add_field(name="Commands Category", value="```Music, LevelSystem, VoiceTemp, Moderation, Utils, Guilds```")
        
        await ctx.send(embed=choose)
        msg = await client.wait_for('message', check=lambda message:message.author == ctx.author and message.channel == ctx.channel, timeout=10)
        
        try:
            if msg.content in args1:
                musics = discord.Embed(
                    title="--- Music Commands ---",
                    color=discord.Color.green()
                )
                musics.add_field(name="Music Commands List", value=str("```" + ", ".join(list1) + "```"))
                musics.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                
                await ctx.send(embed=musics)
            if msg.content in args2:
                lvlsys = discord.Embed(
                    title="--- LevelSystem Commands ---",
                    color=discord.Color.green()
                )
                lvlsys.add_field(name="LevelSystem Commands List", value=str("```" + ", ".join(list2) + "```"))
                lvlsys.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                
                await ctx.send(embed=lvlsys)
            if msg.content in args3:
                vctemp = discord.Embed(
                    title="--- VoiceTemp Commands ---",
                    color=discord.Color.green()
                )
                vctemp.add_field(name="VoiceTemp Commands List", value=str("```" + ", ".join(list3) + "```"))
                vctemp.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                
                await ctx.send(embed=vctemp)
            if msg.content in args4:
                mods = discord.Embed(
                    title="--- Moderation Commands ---",
                    color=discord.Color.green()
                )
                mods.add_field(name="Moderation Commands List", value=str("```" + ", ".join(list4) + "```"))
                mods.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                
                await ctx.send(embed=mods)
            if msg.content in args5:
                utils1 = discord.Embed(
                    title="--- Utils Commands ---",
                    color=discord.Color.green()
                )
                utils1.add_field(name="Utils Commands List", value=str("```" + ", ".join(list5) + "```"))
                utils1.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                
                await ctx.send(embed=utils1)
            if msg.content in args6:
                guilds1 = discord.Embed(
                    title="--- Guilds Commands ---",
                    color=discord.Color.green()
                )
                guilds1.add_field(name="Guilds Commands List", value=str("```" + ", ".join(list6) + "```"))
                guilds1.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                
                await ctx.send(embed=lvlsys)
            else:
                return await ctx.send("Invalid Options. Command Ignored")
        except asyncio.TimeoutError:
            return await ctx.send("Request Timed Out (Timeout: 10 Seconds)")
    elif str(sub) is not None:
        try:
            listc = [cogs, cogs2, cogs3, cogs4, cogs5, cogs6, client.commands]
            
            for comm in len(listc):
                for commn in comm.get_commands(sub):
                    comms = discord.Embed(
                        title="--- Commands Help ---",
                        color=discord.Color.purple()
                    )
                    comms.add_field(name=f"```{sub}``` Command", value=f"Help: {commn.help}")
                    comms.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                    
                    await ctxml.send(embed=comms)
        except Exception:
            return await ctx.send("Command Not Found. Ignored")
    else:
        return await ctx.send("Invalid Options. Command Ignored")

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
client.run(CONFIG['token'])
