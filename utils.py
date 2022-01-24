import discord
from discord.ext import commands
from datetime import datetime
import random
import os
import psutil
import json
import pytz
import requests
import time
import asyncio
from config import CONFIG
from imgapi import SFW, NSFW, MEME, WELCOME
from msg_channel import CHANNEL
from custom_msg import W_MESSAGE, H_MESSAGE, B_MESSAGE, S_MESSAGE, M_MESSAGE, K_MESSAGE, J_MESSAGE, N_MESSAGE

class Utils(commands.Cog):
    """Utils related commands. """
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def waifu(self, ctx, member : discord.Member=None):
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
        mvar = random.choice(list(W_MESSAGE.values()))
        desc = mvar.format(member.mention)
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Random Waifu Image ---",
            description=desc,
            timestamp=ctx.message.created_at
        )
        embed.set_image(url=img_url)
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
                
        await ctx.send(embed=embed)
        sleeper=5
        await asyncio.sleep(sleeper)
        await ctx.message.delete()
    
    @commands.command()
    async def hentai(self, ctx):
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
            mvar = random.choice(list(H_MESSAGE.values()))
            desc = mvar.format(ctx.author.mention)
            embed = discord.Embed(
                color=discord.Color.green(),
                title="--- 18+ Hentai Image ---",
                description=desc,
                timestamp=ctx.message.created_at
            )
            embed.set_image(url=random.choice(imgdata))
            embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
                    
            await ctx.send(embed=embed)
            sleeper=5
            await asyncio.sleep(sleeper)
            await ctx.message.delete()
        else:
            await ctx.send('Note: Write this command in NSFW channel')
            sleeper=5
            await asyncio.sleep(sleeper)
            await ctx.message.delete()
    
    @commands.command()
    async def kiss(self, ctx, member : discord.Member=None):
        """Give your partner a kiss"""
        if member is None:
            await ctx.send("Note: No G*Y/Selfkiss!!! You must tag someone for your kiss partner")
            await ctx.message.delete()
            return
        url7 = SFW['kiss1']
        r7 = requests.get(url7)
        data7 = r7.json()
        imgdata = data7['url']
        mvar = random.choice(list(K_MESSAGE.values()))
        desc = mvar.format(ctx.message.author.mention, member.mention)
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Kiss for You ---",
            description=desc,
            timestamp=ctx.message.created_at
        )
            
        embed.set_image(url=imgdata)
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
        sleeper=5
        await asyncio.sleep(sleeper)
        await ctx.message.delete()
    
    @commands.command()
    async def slap(self, ctx, member : discord.Member=None):
        """Slaps your friend or yourself"""
        if member is None:
            member = ctx.author
        url4 = SFW['slap1']
        r4 = requests.get(url4)
        data4 = r4.json()
        imgdata = data4['url']
        mvar = random.choice(list(S_MESSAGE.values()))
        desc = mvar.format(ctx.message.author.mention, member.mention)
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Slap Someone ---",
            description=desc,
            timestamp=ctx.message.created_at
        )
        embed.set_image(url=imgdata)
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
        sleeper=5
        await asyncio.sleep(sleeper)
        await ctx.message.delete()
    
    @commands.command()
    async def bonk(self, ctx, member : discord.Member=None):
        """Bonk your friends or yourself"""
        if member is None:
            member = ctx.author
        url5 = SFW['bonk1']
        r5 = requests.get(url5)
        data5 = r5.json()
        imgdata = data5['url']
        mvar = random.choice(list(B_MESSAGE.values()))
        desc = mvar.format(ctx.message.author.mention, member.mention)
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Bonk!! ---",
            description=desc,
            timestamp=ctx.message.created_at
        )
        embed.set_image(url=imgdata)
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
                
        await ctx.send(embed=embed)
        sleeper=5
        await asyncio.sleep(sleeper)
        await ctx.message.delete()
    
    @commands.command()
    async def neko(self, ctx, member: discord.Member=None):
        
        url8 = SFW['neko1']
        r8 = requests.get(url8)
        data8 = r8.json()
        imgdata = data8['url']
        
        mvar = random.choice(list(N_MESSAGE.values()))
        desc = mvar.format(ctx.message.author.mention)
        
        if member is None:
            embed = discord.Embed(
                title="--- Cute Neko Image ---",
                description=desc,
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            embed.set_image(url=imgdata)
            embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title="--- Cute Neko Image ---",
                description=str(N_MESSAGE['n_msg2']).format(ctx.message.author.mention, member.mention)
            )
            embed.set_image(url=imgdata)
            embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            
            await ctx.send(embed=embed)
    
    @commands.command()
    async def meme(self, ctx):
        """Random Meme Image"""
        url6 = MEME['meme1']
        r6 = requests.get(url6)
        data6 = r6.json()
        imgdata = data6['url']
        embed = discord.Embed(
            color=discord.Color.green(),
            title=data6['title'],
            timestamp=ctx.message.created_at
        )
        embed.set_image(url=imgdata)
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
        sleeper=5
        await asyncio.sleep(sleeper)
        await ctx.message.delete()
    
    @commands.command() #ping
    async def ping(self, ctx):
        """Showing Bot Latency and YouTube Server Status"""
        start_time = time.time()
        msg = await ctx.send('Testing Connection...')
        end_time = time.time()
        
        pings = requests.get("https://youtube.com")
        status = pings.status_code
        
        if status == 200:
            result = "Online/Active"
        else:
            result = "Error/Inactive"
        
        titles = "Pong!!"
        selflatency = str(f" {round((start_time - end_time) * 1000)}ms")
        botlatency = str(f" {round(self.client.latency * 1000)}ms")
        ytlatency = str(f" {result}")
        embed = discord.Embed(
            title=titles,
            color=ctx.author.color,
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="Your Latency", value=selflatency)
        embed.add_field(name="Client Latency", value=botlatency)
        embed.add_field(name="YouTube Server Status", value=ytlatency)
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
        
        await asyncio.sleep(0.8)
        await msg.delete()
        await ctx.send(embed=embed)
    
    @commands.command() #current_time
    async def time(self, ctx):
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
    
    @commands.command() #supported_link
    async def supported(self, ctx):
        """Checking supported music links"""
        titles = "Supported Platform for Music Player"
        desc = "=> YouTube Link\n=> SoundCloud Link"
        author = ctx.message.author.name
        embed = discord.Embed(
            title=titles,
            description=desc,
            timestamp=ctx.message.created_at
        )
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
    
    @commands.command(name="clean")
    async def _clean(self, ctx, limit: int=None, member: discord.Member=None):
        """Clearing mentioned user messages"""
        await ctx.message.delete()
        msg = []
        try:
            limit = int(limit)
        except:
            fail1 = discord.Embed(
                title="",
                description="Set amount of messages to delete. Example: >clean 100 user[Optional]",
                color=discord.Color.red()
            )
            
            return await ctx.send(embed=fail1)
        
        if not member:
            await ctx.channel.purge(limit=limit)
            done = await ctx.send(f"Purged {limit} messages")
            await asyncio.sleep(10)
            await done.delete()
            return
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        done = await ctx.send(f"Purged {limit} messages of {member.mention}")
        await asyncio.sleep(10)
        await done.delete()
    
    @commands.command(name="avatar") #avatar_command
    async def avatar_(self, ctx, avamem : discord.Member=None):
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
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
    
    @commands.command()
    async def serverinfo(self, ctx):
        """Get Current Server Information"""
        member = ctx.guild.owner
        role_count = len(ctx.guild.roles)
        roles = [role.mention for role in ctx.guild.roles]
        list_of_bots = [bot.mention for bot in ctx.guild.members if bot.bot]
            
        embed2 = discord.Embed(timestamp=ctx.message.created_at, color=ctx.author.color)
        embed2.add_field(name='ID', value=f'{ctx.guild.id}')
        embed2.add_field(name='Name', value=f"{ctx.guild.name}", inline=False)
        embed2.add_field(name='Owner', value=f"{member.name + '#' + member.discriminator}", inline=False)
        embed2.add_field(name='Verification Level', value=str(ctx.guild.verification_level).capitalize(), inline=False)
        embed2.add_field(name='Channel', value=f'{len(ctx.guild.text_channels)} Text / {len(ctx.guild.voice_channels)} Voice', inline=False)
        embed2.add_field(name='Number Of Members', value=ctx.guild.member_count, inline=False)
        embed2.add_field(name=f'Roles ({str(role_count)})', value=(', '.join(roles)), inline=False)
        embed2.add_field(name=f'Bots ({str(len(list_of_bots))})', value=(', '.join(list_of_bots)), inline=False)
        embed2.add_field(name='Created At', value=ctx.guild.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        embed2.set_thumbnail(url=ctx.guild.icon_url)
        embed2.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed2)
    
    @commands.command()
    async def botinfo(self, ctx):
        """Bot Information"""
        botdev = self.client.get_user(843132313562513408)
        current_guild = len(self.client.guilds)
        embed = discord.Embed(
            color=ctx.author.color,
            title="--- Bot Information ---",
            timestamp=ctx.message.created_at
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Bot Name", value=f"{self.client.user.mention}", inline=False)
        embed.add_field(name="Real Bot Name", value="Music Player.py#6361", inline=False)
        embed.add_field(name="Bot Author", value=f"{botdev.mention}", inline=False)
        embed.add_field(name='Created At', value=self.client.user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        embed.add_field(name="Coded in", value="Python3 (discord.py Module)", inline=False)
        embed.add_field(name="Serving on", value=f"{current_guild} Servers", inline=False)
        embed.add_field(name="Bot Category", value="Music Bot (Soon, this bot will be a MultiPurpose bot)", inline=False)
        embed.add_field(name="Auxiliaries", value="Heroku Server (So that bots can always be online)", inline=False)
        embed.add_field(name="Available Commands", value="Check using >help or .help", inline=False)
        embed.set_footer(text="Requested by {}".format(ctx.message.author.name + '#' + ctx.message.author.discriminator), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=embed)
    
    
    @commands.command()
    async def userinfo(self, ctx, member : discord.Member=None):
        """Get User Information"""
        if member is None:
            member = ctx.author
        
        rolelist = [r.mention for r in member.roles if r != ctx.guild.default_role]
        
        text = "No Roles..." if len(rolelist) == 0 else ', '.join(rolelist)
        
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
        embed.add_field(name="User Roles", value=f"{text}")
        embed.set_footer(text=f"Created at {member.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S')} UTC")
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def sendto(self, ctx, member : discord.Member=None, *, arg=None):
        """Send Message to Spesific User using Bot"""
        if member is None or member is ctx.message.author:
            await ctx.send("You can't send DM to yourself")
            return
        if arg is None:
            await ctx.send("Please, write your message")
            return
        else:
            embed = discord.Embed(
                timestamp=ctx.message.created_at,
                color=discord.Color.purple(),
                title="--- Someone DM You ---",
                description=f"From {ctx.message.author.name + '#' + ctx.message.author.discriminator} to {member.name + '#' + member.discriminator}"
            )
            embed.set_thumbnail(url=ctx.message.author.avatar_url)
            embed.add_field(name="This is the message", value=arg)
            
            
            embed1 = discord.Embed(
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            embed1.set_thumbnail(url=member.avatar_url)
            embed1.add_field(name=f"✔ The message has been sent.", value=f"Sent to: `{member.name + '#' + member.discriminator}`")
            
            await ctx.message.delete()
            done = await ctx.send(embed=embed1)
            await asyncio.sleep(2)
            await done.delete()
            await member.send(embed=embed)
    
    @commands.command()
    async def invite(self, ctx, *, uses=None):
        """Create Instant Invite Link"""
        guild = ctx.guild.name
        if uses is None:
            return await ctx.send("Insert Max Used value (0 for Unlimited Use). Example: >invite 5(Limit Link can Used: 5Times/5User)")
        link = await ctx.channel.create_invite(xkcd=True, max_age = 0, max_uses = int(uses))
        embed = discord.Embed(
            color=discord.Color.purple(),
            title="--- Instant Invite Link ---",
            description="Share this invite link to another user"
        )
        embed.add_field(name="This invite link will be redirected to: ", value=guild)
        embed.add_field(name="Max Uses", value=uses)
        embed.add_field(name="This your invite link", value=f"[Hold for Copy the link]({link})")
        
        await ctx.message.delete()
        await ctx.send(embed=embed)
    
    @commands.command()
    async def invitebot(self, ctx):
        """Invite Me!!!"""
        link = "https://discord.com/api/oauth2/authorize?client_id=904156026851455006&permissions=8&scope=bot%20applications.commands"
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Invite Link ---"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Click the link below to invite me to your server!", value=f"[Invite Me!]({link})")
        
        await ctx.send(embed=embed)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def devjoin(self, ctx, *, ids: int=None):
        botdev = self.client.get_user(843132313562513408)
        
        guilds = self.client.get_guild(int(ids))
        
        if ids is None:
            return await ctx.send("Guild not Found")
        
        else:
            ch = random.choice(guilds.channels)
            link = await ch.create_invite(xkcd=True, max_age = 0)
            embed = discord.Embed(
                title="--- Dev Command ---",
                color=discord.Color.green()
            )
            embed.add_field(name="Guild Author", value=f"{guilds.owner.name}")
            embed.add_field(name="Here the Link", value=f"[Click This]({link})")
            await ctx.send(embed=embed)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def showguild(self, ctx):
        botdev = self.client.get_user(843132313562513408)
        
        current_guild = len(self.client.guilds)
        
        for curr in self.client.guilds:
            curguild = discord.Embed(
                title="--- Dev Command ---",
                description=f"Serving on {str(current_guild)}",
                color=discord.Color.green()
            )
            curguild.add_field(name="Guild name", value=", ".join(curr.name))
            curguild.add_field(name="Guild ID", value=f"{str(curr.id)}")
            
            await ctx.send(embed=curguild)
    
    @commands.command()
    async def report(self, ctx, *, reason=None):
        """Report your Problem about this Bot"""
        botdev = self.client.get_user(843132313562513408)
        
        if reason is None:
            await ctx.send("Write down Problems or Bugs that have occurred!!")
            return
        
        embed = discord.Embed(
            title="--- Bot Problem Report ---",
            color=discord.Color.purple(),
            timestamp=ctx.message.created_at
        )
        embed.add_field(name="Reported by", value=f"{ctx.message.author.mention}")
        embed.add_field(name="From Server", value=f"{ctx.guild.name}'s server")
        embed.add_field(name="The problem/bugs", value=f"{str(reason)}")
        
        await ctx.send(embed=embed)
        await botdev.send(embed=embed)
    
    @commands.command()
    async def status(self, ctx):
        #=== Memory Identifier ===
        mem=str(os.popen('free -t -m').readlines())
        T_ind=mem.index('T')
        mem_G=mem[T_ind+14:-4]
        S1_ind=mem_G.index(' ')
        mem_T=mem_G[0:S1_ind]
        mem_G1=mem_G[S1_ind+8:]
        S2_ind=mem_G1.index(' ')
        mem_U=mem_G1[0:S2_ind]
        mem_F=mem_G1[S2_ind+8:]
        
        #=== CPU Identifier ===
        vcc=psutil.cpu_count()
        vcpu=psutil.cpu_percent()
        
        result = discord.Embed(
            title="--- Bot Status ---",
            description=f'Total number of CPUs : {str(vcc)}\nTotal CPUs utilized percentage : {str(vcpu)}%\nTotal Memory : {mem_T} MB\nUsed Memory : {mem_U} MB\nFree Memory : {mem_F} MB',
            color=self.client.user.color
        )
        result.set_thumbnail(url=self.client.user.avatar_url)
        
        await ctx.send(embed=result)
    
    @commands.command(hidden=True)
    async def status2(self, ctx):
        em = discord.Embed(type='rich', title = 'System Resource Usage', description = 'See CPU and memory usage of the system.')
        em.add_field(name = 'CPU Usage', value = f'{psutil.cpu_percent()}%', inline = False)
        em.add_field(name = 'Memory Usage', value = f'{psutil.virtual_memory().percent}%', inline = False)
        em.add_field(name = 'Available Memory', value = f"{str(psutil.virtual_memory().available >> 20) + 'MB, From ' + str(psutil.virtual_memory().total >> 20)}", inline = False)
        await ctx.send(embed = em)
    
    @commands.command(aliases=['remindme'])
    async def reminder(self, ctx, times=None, *, args: str=None):
        """
        Set reminder for you.
        """
        if times is None or args is None:
            return await ctx.send("Set reminder for you")
        else:
            settime = 0
            if times:
                if times.endswith('s'):
                    settime = int(times.replace('s', ''))
                elif times.endswith('m'):
                    settime = 60 * int(times.replace('m', ''))
                elif times.endswith('h'):
                    settime = 60 * 60 * int(times.replace('h', ''))
            else:
                return await ctx.send('Set time reminder')
            
            if args:
                done = await ctx.send('Set Reminder for You!')
                await asyncio.sleep(settime)
                await ctx.message.delete()
                await done.delete()
                await ctx.send(f'{ctx.author.mention}, Your reminder: {args}')
            
            else:
                return await ctx.send('Set message reminder!')
    
    @commands.command(hidden=True)
    async def test_tts(self, ctx, *, msg: str=None):
        if msg is None:
            return
        await ctx.reply(msg, tts=True)
    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def repeat(self, ctx, multiplier: int=None, *, message: str=None):
        if multiplier is None or message is None:
            await ctx.message.delete()
            fail = await ctx.send('Failed')
            return await fail.delete()
        
        await ctx.message.delete()
        for i in range(multiplier):
            await ctx.send(message)
    
    #Failed
    @commands.command(aliases=["wiki", "wkpd"], hidden=True)
    async def wikipedia(self, ctx, search: str=None):
        if search is None:
            return
        
        reg = search.replace("", "_").lower()
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{reg}"
        data = requests.get(url).json()
        
        if data['title'] == "Not Found":
            failed = discord.Embed(
                title="",
                description=data['title'],
                color=discord.Color.red()
            )
            return await ctx.send(embed=failed)
        
        desktop = f"https://en.wikipedia.org/wiki/{data['title']}"
        mobile = f"https://en.m.wikipedia.org/wiki/{data['title']}"
        
        result = discord.Embed(
            title=data['title'],
            description=data['extract'],
            color=discord.Color.green()
        )
        result.set_thumbnail(url=data['originalimage']['source'])
        result.add_field(name="For more info", value=f"__Mobile__: [Click Here]({mobile})\n__Desktop__: [Click Here]({desktop})")
        result.set_footer(text=f"Requested by {ctx.author.name} | {datetime.now().strftime('%d-%m-%Y, %H:%M:%S')}")
        
        print(reg)
        await ctx.send(embed=result)

def setup(client):
    client.add_cog(Utils(client))
