import discord
from discord.ext import commands
from datetime import datetime
import random
import json
import pytz
import requests
import time
import asyncio
from config import CONFIG
from imgapi import SFW, NSFW, MEME, WELCOME
from msg_channel import CHANNEL
from custom_msg import W_MESSAGE, H_MESSAGE, B_MESSAGE, S_MESSAGE, M_MESSAGE, K_MESSAGE, J_MESSAGE

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
    
    @commands.command(hidden=True)
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
    
    @commands.command()
    async def slap(self, ctx, member : discord.Member=None):
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
    
    @commands.command()
    async def bonk(self, ctx, member : discord.Member=None):
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
    
    @commands.command()
    async def meme(self, ctx):
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
    
    @commands.command() #ping
    async def ping(self, ctx):
        """Showing Bot Latency and YouTube Server Status"""
        pings = requests.get("https://youtube.com")
        titles = "Pong!!"
        selflatency = str(f" {round(self.client.latency * 1000)}ms")
        ytlatency = str(f" {pings}")
        author = ctx.message.author.name
        embed = discord.Embed(
            title=titles,
        )
        embed.add_field(name="Your Latency", value=selflatency)
        embed.add_field(name="YouTube Server Status", value=ytlatency)
        embed.set_footer(text="Author: {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            
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
        desc = "For Now, Only Support YouTube Link"
        author = ctx.message.author.name
        embed = discord.Embed(
            title=titles,
            description=desc,
        )
        embed.set_footer(text="Author: {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
    
    @commands.command(name="clean")
    async def clean_all(self, ctx, amount: int=None):
        """Clearing messages at once"""
        if amount is None:
            fail1 = discord.Embed(
                title="",
                description="Set amount of messages to delete. Example: >clean 100",
                color=discord.Color.red()
            )
            
            return await ctx.send(embed=fail1)
        
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        done = await ctx.send("👍")
    
    @commands.command(name="clean_user")
    async def clean_us(self, ctx, limit: int=None, member: discord.Member=None):
        """Clearing mentioned user messages"""
        await ctx.message.delete()
        msg = []
        try:
            limit = int(limit)
        except:
            fail1 = discord.Embed(
                title="",
                description="Set amount of messages to delete. Example: >clean 100 [user]",
                color=discord.Color.red()
            )
            
            return await ctx.send(embed=fail1)
        
        if not member:
            await ctx.channel.purge(limit=limit)
            return await ctx.send(f"Purged {limit} messages")
        async for m in ctx.channel.history():
            if len(msg) == limit:
                break
            if m.author == member:
                msg.append(m)
        await ctx.channel.delete_messages(msg)
        await ctx.send(f"Purged {limit} messages of {member.mention}")
    
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
        embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
    
    @commands.command()
    async def serverinfo(self, ctx):
        """Get Current Server Information"""
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
    
    @commands.command()
    async def botinfo(self, ctx):
        """Bot Information"""
        botdev = self.client.get_user(843132313562513408)
        embed = discord.Embed(
            color=ctx.author.color,
            title="--- Bot Information ---"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Bot Name", value=f"{self.client.user.mention}", inline=False)
        embed.add_field(name="Real Bot Name", value="Music Player.py#6361", inline=False)
        embed.add_field(name="Bot Author", value=f"{botdev.mention}", inline=False)
        embed.add_field(name='Created At', value=self.client.user.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'), inline=False)
        embed.add_field(name="Coded in", value="Python3 (discord.py Module)", inline=False)
        embed.add_field(name="Bot Category", value="Music Bot (Soon, this bot will be a MultiPurpose bot)", inline=False)
        embed.add_field(name="Auxiliaries", value="Heroku Server (So that bots can always be online)", inline=False)
        embed.add_field(name="Available Commands", value="Check using >help or .help", inline=False)
        embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
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
    
    @commands.command()
    async def invite(self, ctx, *, uses=None):
        """Create Instant Invite Link"""
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
    
    @commands.command()
    async def invitebot(self, ctx):
        """Invite Me!!!"""
        link = "https://discord.com/api/oauth2/authorize?client_id=904156026851455006&permissions=433103232119&scope=bot%20applications.commands"
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Invite Link ---"
        )
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.add_field(name="Click the link below to invite me to your server!", value=f"[Invite Me!]({link})")
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def report(self, ctx, reason=None):
        """Report your Problem about this Bot"""
        botdev = self.client.get_user(843132313562513408)
        
        if reason is None:
            await ctx.send("Write down Problems or Bugs that have occurred!!")
            return
        
        embed = discord.Embed(
            title="--- Bot Problem Report ---",
            color=discord.Color.purple()
        )
        embed.add_field(name="Reported by", value=f"{ctx.message.author.mention}")
        embed.add_field(name="The problem/bugs", value=f"{str(reason)}")
        embed.set_footer(text="Reported at Today, {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")))
        
        await ctx.send(embed=embed)
        await botdev.send(embed=embed)

def setup(client):
    client.add_cog(Utils(client))
