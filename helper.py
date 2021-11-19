import discord
from discord.ext import commands
import random
import time
import requests
import pytz
from datetime import datetime

class Helper(commands.Cog):
    """Related Commands for Help."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command() #ping
    async def ping(ctx):
        """Showing Bot Latency and YouTube Server Status"""
        pings = requests.get("https://youtube.com")
        titles = "Pong!!"
        selflatency = str(f" {round(self.bot.latency * 1000)}ms")
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
    
    @commands.command() #supported_link
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
    
    @commands.command(name="avatar") #avatar_command
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
    
    @commands.command()
    async def serverinfo(ctx):
        member = ctx.guild.members.guild_permissions.administrator
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
        embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=embed2)

def setup(bot):
    bot.add_cog(Helper(bot))