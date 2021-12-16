import discord
from discord.ext import commands
from datetime import datetime
import pytz

class Voice(commands.Cog):
    """Voice related commands. """
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
        return
        
        if len(before.channel.members) == 0:
           return await before.channel.delete()
    
    #lock
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        """Lock Current Voice Channel"""
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
        """Unlock Current Locked Voice Channel (Failed Program)"""
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
        """Set UserLimit for Current Voice Channel"""
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
            fail2 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail2)
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
        """Set Bitrate for Current Voice Channel"""
        if amount is None:
            return
        if not 7 < amount < 97:
            fail2 = discord.Embed(
                title="",
                description="Enter bitrate value: 8 - 96",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail2)
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
    async def name(self, ctx, *, names=None):
        """Set Name for Current Voice Channel"""
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
    async def listener(self, ctx):
        """Get a List of Listeners at Current Voice Channel"""
        channel = ctx.message.author.voice.channel
        listening = [r.mention for r in channel.members]
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        done = discord.Embed(
            title="--- Voice Channel Listener ---",
            color=discord.Color.green()
        )
        done.add_field(name=f"Listener at {channel.name}", value=", ".join(listening))
        done.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=done)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member=None):
        channel = ctx.message.author.voice.channel
        """Mute Someone on Current Voice Channel"""
        if member is None:
            return
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        if member not in ctx.message.author.voice.channel:
            fail2 = discord.Embed(
                title="",
                description=f"{member.mention} are not in {ctx.message.voice.channel.name}",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail2)
        
        await member.voice.channel.edit(mute=True)
        muted = discord.Embed(
            title="",
            color=discord.Color.red()
        )
        muted.add_field(name=f"Muted in {channel.name}", value=f"User: {member.mention}")
        muted.set_footer(text="Muted by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=muted)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(mute_members=True)
    async def unmute(self, ctx, member: discord.Member=None):
        channel = ctx.message.author.voice.channel
        """Unmute muted User on Current Voice Channel"""
        if member is None:
            return
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        if member not in ctx.message.author.voice.channel:
            fail2 = discord.Embed(
                title="",
                description=f"{member.mention} are not in {ctx.message.voice.channel.name}.",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail2)
        
        await member.voice.channel.edit(mute=False)
        unmuted = discord.Embed(
            title="",
            color=discord.Color.red()
        )
        unmuted.add_field(name=f"Unmuted in {channel.name}", value=f"User: {member.mention}")
        unmuted.set_footer(text="Unmuted by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=muted)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(deafen_members=True)
    async def deafen(self, ctx, member: discord.Member=None):
        """Deafen someone on Current Voice Channel"""
        channel = ctx.message.author.voice.channel
        
        if member is None:
            return
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        if member not in ctx.message.author.voice.channel:
            fail2 = discord.Embed(
                title="",
                description=f"{member.mention} are not in {ctx.message.voice.channel.name}",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail2)
        
        await member.edit(deafen=True)
        deaf = discord.Embed(
            title="",
            color=discord.Color.red()
        )
        deaf.add_field(name=f"Deafened in {channel.name}", value=f"User: {member.mention}")
        deaf.set_footer(text="Deafened by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=deaf)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(deafen_members=True)
    async def undeafen(self, ctx, member: discord.Member=None):
        """Undeafen deafened User on Current Voice Channel"""
        channel = ctx.message.author.voice.channel
        
        if member is None:
            return
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        if member not in ctx.message.author.voice.channel:
            fail2 = discord.Embed(
                title="",
                description=f"{member.mention} are not in {ctx.message.voice.channel.name}",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail2)
        
        await member.edit(deafen=False)
        undeaf = discord.Embed(
            title="",
            color=discord.Color.red()
        )
        undeaf.add_field(name=f"Undeafened in {channel.name}", value=f"User: {member.mention}")
        undeaf.set_footer(text="Undeafened by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=undeaf)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(deafen_members=True)
    async def deafen_all(self, ctx, mode=None):
        """Deafen all users at once on Current Voice Channe"""
        channel = ctx.message.author.voice.channel
        
        deafs = [r.members for r in channel.members if r != ctx.messsage.author]
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        if str(mode) == None:
            fail1 = discord.Embed(
                title="",
                description="Enter deafen_all mode: **true** / **false**",
                color=discord.Color.red()
            )
            await ctx.send(embed=fail1)
        
        if str(mode) == "true":
            for member in deafs:
                await member.voice.channel.edit(deafen=True)
                deaf = discord.Embed(
                    title="",
                    color=discord.Color.red()
                )
                deaf.add_field(name=f"All deafened in {channel.name}", value=f"Deafened by {ctx.message.author.mention}")
                deaf.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=deaf)
        
        if str(mode) == "false":
            for member in deafs:
                await member.voice.channel.edit(deafen=False)
                undeaf = discord.Embed(
                    title="",
                    color=discord.Color.green()
                )
                undeaf.add_field(name=f"All undeafened in {channel.name}", value=f"Undeafened by {ctx.message.author.mention}")
                undeaf.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=undeaf)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(mute_members=True)
    async def mute_all(self, ctx, mode=None):
        """Mute all users at once on Current Voice Channel"""
        channel = ctx.message.author.voice.channel
        mutes = [r.members for r in channel.members if r != ctx.messsage.author]
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        if str(mode) == None:
            fail1 = discord.Embed(
                title="",
                description="Enter mute_all mode: **true** / **false**",
                color=discord.Color.red()
            )
            await ctx.send(embed=fail1)
        
        if str(mode) == "true":
            for member in mutes:
                await member.voice.channel.edit(mute=True)
                muted = discord.Embed(
                    title="",
                    color=discord.Color.red()
                )
                muted.add_field(name=f"All Muted in {channel.name}", value=f"Muted by {ctx.message.author.mention}")
                muted.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=deaf)
        
        if str(mode) == "false":
            for member in mutes:
                await member.voice.channel.edit(mute=False)
                unmute = discord.Embed(
                    title="",
                    color=discord.Color.green()
                )
                unmute.add_field(name=f"All unmuted in {channel.name}", value=f"Unmuted by {ctx.message.author.mention}")
                unmute.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                await ctx.send(embed=unmute)
    
    @commands.command(pass_context=True)
    @commands.has_permissions(manage_channels=True)
    async def region(self, ctx, mode=None):
        """Set Voice Channel Region (Failed Program)"""
        channel = ctx.message.author.voice.channel
        
        if ctx.message.author.voice is None:
            fail1 = discord.Embed(
                title="",
                description="You're not in Voice Channel. Command Ignored",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail1)
        
        if str(mode) == None:
            fail2 = discord.Embed(
                title="",
                description="Enter Voice Region name!!",
                color=discord.Color.green()
            )
            fail2.add_field(name="List of Voice Region Name", value="automatic, amsterdam, brazil, dubai, eu_central, eu_west, europe, frankurt, hongkong, india, japan, london, russia, singapore, southafrica, south_korea, sydney, us_central, us_east, us_south, us_west")
            return await ctx.send(embed=fail2)
        
        await channel.edit(rtc_region=f'{mode}')
        done = discord.Embed(
            title="",
            description=f"Voice Region has been set to ```{str(mode)}```"
        )
        done.set_footer(text="Today at {}".format(datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed=done)

def setup(client):
    client.add_cog(Voice(client))
