import discord
from discord.ext import commands
from datetime import datetime
import pytz

class Voice(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        person_freq=['1', '2', '3']
        person = member.name
        
        if member.bot:
            return
        if str(after.channel) == "buat baru":
            if str(after) != str(before):
                guild = member.guild
                freq = person_freq[0]
                act_voice_channels = (c.name for c in guild.voice_channels)
                for freq in person_freq:
                    if freq not in act_voice_channels:
                        await after.channel.clone(name=freq)
                        channel = discord.utils.get(guild.voice_channels, name=freq)
                        await member.move_to(channel)
                        return
        await member.guild.create_voice_channel(name="buat baru")
        return
        
        if len(before.channel.members) == 0:
            await before.channel.delete()
    
    #lock
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        await ctx.channel.purge(limit=1)
        channel = ctx.message.author.voice.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.connect = False
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        done = discord.Embed(
            title="",
            description="🔒 Channel Locked",
            color=discord.Color.green()
        )
        done.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=done)
    
    
    #unlock
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        await ctx.channel.purge(limit=1)
        channel = ctx.message.author.voice.channel
        overwrite = channel.overwrites_for(ctx.guild.default_role)
        overwrite.connect = True
        await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        done = discord.Embed(
            title="",
            description="🔓 Channel Unlocked",
            color=discord.Color.green()
        )
        done.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=done)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def userlimit(self, ctx, amount: int=None):
        
        if amount is None:
            return
        if not 1 < amount < 51:
            fail1 = discord.Embed(
                title="",
                description="Enter limit value: 2 - 50.",
                color=discord.Color.green()
            )
            await ctx.send(embed=fail1)
            return
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        else:
            channel = ctx.message.author.voice.channel
            await channel.edit(user_limit=amount)
            done = discord.Embed(
                title="",
                description=f"User Limit has been set to {amount}",
                color=discord.Color.green()
            )
            done.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=done)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def bitrate(self, ctx, amount: int=None):
        
        if amount is None:
            return
        if not 7 < amount < 97:
            fail1 = discord.Embed(
                title="",
                description="Enter bitrate value: 8 - 96",
                color=discord.Color.green()
            )
            await ctx.send(embed=fail1)
            return
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        else:
            channel = ctx.message.author.voice.channel
            await channel.edit(bitrate=int(round(amount * 1000)))
            done = discord.Embed(
                title="",
                description=f"Bitrate has been set to {amount}Kbps",
                color=discord.Color.green()
            )
            done.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=done)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def name(self, ctx, names=None):
        
        if names is None:
            fail1 = discord.Embed(
                  title="",
                  description="Set your voice channel name!!",
                  color=discord.Color.green()
              )
            return await ctx.send(embed=fail1)
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        else:
            channel = ctx.message.author.voice.channel
            await channel.edit(name=str(names))
            done = discord.Embed(
                title="",
                description=f"Channel name has been set to {str(names)}",
                color=discord.Color.green()
            )
            done.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            await ctx.send(embed=done)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def listener(self, ctx):
        channel = ctx.message.author.voice.channel
        listening = [r.mention for r in channel.members if r != ctx.author.bot]
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        done = discord.Embed(
            title="--- Channel Listener ---",
            color=discord.Color.green()
        )
        done.add_field(name=f"Listener at {channel.name}", value=", ".join(listening))
        done.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=done)

def setup(client):
    client.add_cog(Voice(client))
