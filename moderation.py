import discord
from discord.ext import commands
import asyncio
import pytz
from datetime import datetime

class Moderator(commands.Cog):
    """Moderator related commands. """
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def changename(self, ctx, names=None):
        """Change Nickname for Yourself"""
        if names is None:
            fail1 = discord.Embed(
                title="--- Change Name ---",
                color=discord.Color.red()
            )
            fail1.add_field(name="Change Status", value="Failed!!")
            return await ctx.send(embed=fail1)
        
        changed = discord.Embed(
            title="--- Change Name ---",
            color=discord.Color.purple()
        )
        changed.add_field(name="Change Status", value="Completed!!")
        changed.add_field(name="Name (Before)", value=f"{ctx.message.author.name}")
        changed.add_field(name="Name (After)", value=f"{names}")
        changed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=changed)
        await asyncio.sleep(2)
        await ctx.message.author.edit(nick=str(names))
    
    @commands.command()
    @commands.has_permissions(manage_guild=True, ban_members=True, kick_members=True)
    async def ban(self, ctx, member : discord.Member=None, *, reason=None):
        try:
            yes = ["y", "yes", "Y"]
            no = ["n", "no", "N"]
            
            if reason is None:
                await ctx.send("Reason required!!")
                return
            if member is ctx.guild.owner and member != None:
                await ctx.send("Owner!!. You can't ban Server Owner")
                return
            if member is None:
                await ctx.send("You have to choose a member to get banned. Command Ignored")
                return
            
            confirm = discord.Embed(
                title="",
                description=f"Are you sure you want to ban {member.mention}? (y/n)",
                color=discord.Color.magenta()
            )
            
            await ctx.send(embed=confirm)
            msg = await self.client.wait_for('message', check=lambda message : message.author == ctx.author and message.channel == ctx.channel)
            if msg.content in yes:
                guild = ctx.guild.name
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="--- Banned Member ---",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                embed.add_field(name="Member Name", value=f"{member.mention}")
                embed.add_field(name="Punishment", value="Banned from Server")
                embed.add_field(name="Reason", value=f"{reason}")
                embed.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
                
                banned = discord.Embed(
                    title="--- You have been Banned ---",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                banned.add_field(name="Punishment", value="Banned from Server")
                banned.add_field(name="Reason", value=f"{reason}")
                banned.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
                
                await ctx.send(embed=embed)
                await ctx.send("✔ User has been notified.")
                await member.send(embed=banned)
            
            elif msg.content in no:
                cancelled = discord.Embed(
                    title="",
                    description=f"Ban {member.mention} cancelled",
                    color=discord.Color.green()
                )
                
                await ctx.send(embed=cancelled)
        except asyncio.TimeoutError:
            failed = discord.Embed(
                title="",
                description="Ban Timeout",
                color=discord.Color.red()
            )
            return await ctx.send(embed=failed)
    
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permission(s) to run this command.")
        else:
            raise error
    
    @commands.command()
    @commands.has_permissions(manage_guild=True, kick_members=True)
    async def kick(self, ctx, member : discord.Member=None, *, reason=None):
        try:
            yes = ["y", "yes", "Y"]
            no = ["n", "no", "N"]
            
            if reason is None:
                await ctx.send("Reason required!!")
                return
            if member is ctx.guild.owner and member != None:
                await ctx.send("Owner!!. You can't kick Server Owner")
                return
            
            confirm = discord.Embed(
                title="",
                description=f"Are you sure you want to kick {member.mention}? (y/n)",
                color=discord.Color.magenta()
            )
            
            await ctx.send(embed=confirm)
            msg = await self.client.wait_for('message', check=lambda message : message.author == ctx.author and message.channel == ctx.channel)
            if msg.content in yes:
                guild = ctx.guild.name
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="--- Kicked Member ---",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_a
                )
                embed.add_field(name="Member Name", value=f"{member.mention}")
                embed.add_field(name="Punishment", value="Kicked from Server")
                embed.add_field(name="Reason", value=f"{reason}")
                embed.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
                
                kicked = discord.Embed(
                    title="--- You have been Kicked ---",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                kicked.add_field(name="Punishment", value="Kicked from Server")
                kicked.add_field(name="Reason", value=f"{reason}")
                kicked.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
                
                await ctx.send(embed=embed)
                await ctx.send("✔ User has been notified.")
                await member.send(embed=kicked)
            
            elif msg.content in no:
                cancelled = discord.Embed(
                    title="",
                    description=f"Kick {member.mention} cancelled",
                    color=discord.Color.green()
                )
                
                await ctx.send(embed=cancelled)
        except asyncio.TimeoutError:
            failed = discord.Embed(
                title="",
                description="Kick Timeout!!"
            )
            return await ctx.send(embed=failed)
    
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permission(s) to run this command.")
        else:
            raise error

def setup(client):
    client.add_cog(Moderator(client))
