import discord
import discord
from discord.ext import commands
from discord import VoiceRegion
from pymongo import MongoClient
from typing import Union
import asyncio
import random
import string
from datetime import datetime
from config import CONFIG

white = {
    'r': 255,
    'g': 255,
    'b': 255
}

dataclient = MongoClient(CONFIG['mongodb_url'])
database = dataclient['database8']
saved = database['voice']
saved_guild = database['guild_vc']

#Soon
def generate_password(length=8):
    result = ''.join(
        random.choice(string.ascii_letters) for _ in range(length)
    )
    return result

class VoiceVoteManager:
    def __init__(
        self,
        ctx: commands.Context
    ):
        self.ctx = ctx
    
    async def start_votekick(
        self,
        member: discord.Member,
        channel: discord.VoiceChannel,
        timeout: int
    ):
        voting = discord.Embed(
            title='--- Vote Kick ---',
            description=f"Waiting vote to kick {member.mention}\n{str(timeout)} Seconds from now\nCurrent member can vote in {channel.mention}: {len(channel.members)}",
            color=discord.Color.blurple()
        )
        
        vote = await self.ctx.send(embed=voting)
        await vote.add_reaction(':white_check_mark:')
        await vote.add_reaction(':x:')
        await asyncio.sleep(timeout)
        
        embvoteend = discord.Embed(
            description='Voting is done!!.\nCounting result...',
            color=discord.Color.green()
        )
        voteend = await self.ctx.send(embed=embvoteend)
        
        yes = vote.reactions[0].count
        no = vote.reactions[1].count
        
        await voteend.delete()
        raw_res = discord.Embed(
            title='--- Vote Result ---',
            description=f'Yes: {yes}\nNo: {no}',
            color=discord.Color.purple()
        )
        await self.ctx.send(embed=raw_res)
        await asyncio.sleep(3)
        
        if yes > no:
            await member.move_to(None)
            result = discord.Embed(
                title='',
                description=f'{member.mention} has been kicked from your channel',
                color=discord.Color.purple()
            )
        elif yes < no or yes == no:
            result = discord.Embed(
                title='',
                description=f'Kick {member.mention} from your channel cancelled',
                color=discord.Color.purple()
            )
        await self.ctx.send(embed=result)
    
    async def start_voteban(
        self,
        member: discord.Member,
        channel: discord.VoiceChannel,
        timeout: int
    ):
        voting = discord.Embed(
            title='--- Vote Ban ---',
            description=f"Waiting vote to ban {member.mention}\n{str(timeout)} Seconds from now\nCurrent member can vote in {channel.mention}: {len(channel.members)}",
            color=discord.Color.blurple()
        )
        
        vote = await self.ctx.send(embed=voting)
        await vote.add_reaction(':white_check_mark:')
        await vote.add_reaction(':x:')
        await asyncio.sleep(timeout)
        
        embvoteend = discord.Embed(
            description='Voting is done!!.\nCounting result...',
            color=discord.Color.green()
        )
        voteend = await self.ctx.send(embed=embvoteend)
        
        yes = vote.reactions[0].count
        no = vote.reactions[1].count
        
        await voteend.delete()
        raw_res = discord.Embed(
            title='--- Vote Result ---',
            description=f'Yes: {yes}\nNo: {no}',
            color=discord.Color.purple()
        )
        await self.ctx.send(embed=raw_res)
        await asyncio.sleep(3)
        
        if yes > no:
            await member.move_to(None)
            result = discord.Embed(
                title='',
                description=f'{member.mention} has been banned from your channel',
                color=discord.Color.purple()
            )
        elif yes < no or yes == no:
            result = discord.Embed(
                title='',
                description=f'Ban {member.mention} from your channel cancelled',
                color=discord.Color.purple()
            )
        await self.ctx.send(embed=result)

class VoiceV2(commands.Cog):
    def __init__(self, client: commands.Bot): 
        self.client = client
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        data = saved.find_one({
            'authorID': member.id
        })
        
        guildSettings = saved_guild.find_one({
            'guildID': member.guild.id,
            'ownerID': member.guild.owner.id
        })
        if guildSettings is None:
            pass
        else:
            voiceID = guildSettings['voiceID']
            try:
                if after.channel.id == voiceID:
                    categoryID = guildSettings['categoryID']
                    
                    if data is not None:
                        name = data['channelName']
                        bitrate = data['channelBitrate']
                        limit = data['userLimit']
                    else:
                        name = f"{member.name}'s Channel"
                        bitrate = 64000
                        limit = 0
                   
                    category = self.client.get_channel(categoryID)
                    channel2 = await member.guild.create_voice_channel(name, category=category)
                    await member.move_to(channel2)
                    await channel2.set_permissions(self.client.user, connect=True, read_messages=True)
                    await channel2.edit(name=name, user_limit=limit, bitrate=bitrate)
                    
                    if data is None:
                        saved.insert_one({
                            'guildID': member.guild.id,
                            'authorID': member.id,
                            'channelID': channel2.id,
                            'channelName': name,
                            'channelBitrate': bitrate,
                            'userLimit': limit
                        })
                    else:
                        saved.update_one({'authorID': member.id}, {'$set': {'channelID': channel2.id}})
                    
                    def check(a,b,c):
                        return len(channel2.members) == 0
                    await self.client.wait_for('voice_state_update', check=check)
                    await channel2.delete()
                    await asyncio.sleep(5)
                    if data['keepSettings'] == 'true':
                        return
                    saved.delete_one({
                        'authorID': member.id
                    })
            except:
                pass
    
    @commands.command(
        name='v-fetch_id',
        aliases=['v-get_id']
    )
    @commands.has_permissions(
        manage_guild=True
    )
    async def fetch_id(self, ctx: commands.Context, *, channel: discord.VoiceChannel=None):
        """
        Get current voice channel ID.
        """
        if channel is None:
            channel = ctx.author.voice.channel
        try:
            target_ch = self.client.get_channel(channel.id)
        except commands.ChannelNotFound:
            failed = discord.Embed(
                title='',
                description='Channel Not Found!!',
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=failed)
        else:
            done = discord.Embed(
                title='',
                description=f'{target_ch.mention} ID is {target_ch.id}',
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-setup'
    )
    @commands.has_permissions(
        administrator=True,
        manage_guild=True
    )
    async def _setup(self, ctx: commands.Context):
        """
        Setup for temporary voice channel.
        """
        data = saved_guild.find_one({
            'guildID': ctx.guild.id
        })
        
        start_question = discord.Embed(
            title='',
            description='You have 60 seconds to answer each question!',
            color=discord.Color.purple()
        )
        first_question = discord.Embed(
            title='',
            description='Enter the ID of the category that you have created',
            color=discord.Color.purple()
        )
        await ctx.send(embed=start_question)
        await asyncio.sleep(2)
        await ctx.send(embed=first_question)
        try:
            category = await self.client.wait_for(
                'message',
                check=lambda message:message.author == ctx.author and message.channel == ctx.channel,
                timeout=60
            )
        except asyncio.TimeoutError:
            fail = discord.Embed(
                title='',
                description='Question Timed out',
                color=discord.Color.red()
            )
            return await ctx.send(embed=fail)
        else:
            try:
                get_cat = self.client.get_channel(int(category.content))
            except commands.ChannelNotFound:
                fail = discord.Embed(
                    title='',
                    description='Category Not Found',
                    color=discord.Color.red()
                )
                return await ctx.send(embed=fail)
            if not isinstance(get_cat.type, discord.ChannelType.category):
                fail = discord.Embed(
                    title='',
                    description='This is not a category!',
                    color=discord.Color.red()
                )
                return await ctx.send(embed=fail)
            else:
                second_question = discord.Embed(
                    title='',
                    description='Enter the name of the voice channel that you have created (Make sure the channel in the same category)',
                    color=discord.Color.purple()
                )
                await ctx.send(embed=second_question)
                try:
                    channel = await self.client.wait_for(
                        'message',
                        check=lambda message:message.author == ctx.author and message.channel == ctx.channel,
                        timeout=60
                    )
                except asyncio.TimeoutError:
                    fail = discord.Embed(
                        title='',
                        description='Question Timed out',
                        color=discord.Color.red()
                    )
                    return await ctx.send(embed=fail)
                else:
                    try:
                        get_ch = self.client.get_channel(int(channel.content))
                    except commands.ChannelNotFound:
                        fail = discord.Embed(
                            title='',
                            description='Channel Not Found',
                            color=discord.Color.red()
                        )
                        return await ctx.send(embed=fail)
                    if not isinstance(get_ch.type, discord.ChannelType.voice):
                        fail = discord.Embed(
                            title='',
                            description='This is not a voice channel!',
                            color=discord.Color.red()
                        )
                        return await ctx.send(embed=fail)
                    else:
                        if data is None:
                            new_data = {
                                'guildID': ctx.guild.id,
                                'ownerID': ctx.guild.owner.id,
                                'voiceID': get_ch.id,
                                'categoryID': get_cat.id
                            }
                            saved_guild.insert_one(new_data)
                            done = discord.Embed(
                                title='',
                                description='All setup has completed and ready to go!',
                                color=discord.Color.purple()
                            )
                            await ctx.send(embed=done)
                        else:
                            saved_guild.update_one({'guildID': ctx.guild.id}, {'$set': {'voiceID': get_ch.id, 'categoryID': get_cat.id}}, upsert=True)
                            done = discord.Embed(
                                title='',
                                description='(Updated) All setup has completed and ready to go!',
                                color=discord.Color.purple()
                            )
                            await ctx.send(embed=done)
    
    @commands.command(
        name='v-userlimit',
        aliases=['v-ul', 'v-limit']
    )
    async def _userlimit(self, ctx: commands.Context, limit: int=None):
        """
        Sets limit how many users can join the channel (0 for unlimited).
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif limit < 0:
            fail = discord.Embed(
                title='',
                description="Invalid Number!!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            await channel.edit(user_limit=limit)
            saved.update_one({'authorID': ctx.author.id}, {'$set': {'userLimit': limit}}, upsert=True)
            if limit == 0:
                done = discord.Embed(
                    title='',
                    description=f'User limit has been set to `No Limit`',
                    color=discord.Color.green(),
                    timestamp=ctx.message.created_at
                )
            else:
                done = discord.Embed(
                    title='',
                    description=f'User limit has been set to `{limit} User`',
                    color=discord.Color.green(),
                    timestamp=ctx.message.created_at
                )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-name',
        aliases=['v-changename', 'v-rename']
    )
    async def _name(self, ctx: commands.Context, *, name):
        """
        Modifies the channel name.
        Custom type:
          - `default`: Set name by default (your Discord Username)
          - `guild`: Set name by guild/server name
          - `tag`: Set name by your tag (#0000)
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            
            set_name = name
            if name.lower() == 'default':
                set_name = ctx.author.display_name
            elif name.lower() == 'guild':
                set_name = ctx.guild.name
            elif name.lower() == 'tag':
                set_name = ctx.author.discriminator
            else:
                set_name = name
            
            await channel.edit(name=set_name)
            saved.update_one({'authorID': ctx.author.id}, {'$set': {'channelName': set_name}}, upsert=True)
            done = discord.Embed(
                title='',
                description=f"Channel name has been changed to `{set_name}`",
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-ban',
        aliases=['v-banuser']
    )
    async def _ban(self, ctx: commands.Context, member: discord.Member=None):
        """
        Bans a specific user from the voice channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description=f"Please specify a user to banned",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            member_list = [mem.id for mem in channel.members]
            if member.id not in member_list:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            await member.move_to(None)
            overwrite = channel.overwrites_for(member)
            overwrite.connect = False
            await channel.set_permissions(member, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description=f'{member.mention} has been banned from your channel',
                color=discord.Color.purple(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-unban',
        aliases=['v-unbanuser']
    )
    async def _unban(self, ctx: commands.Context, member: discord.Member=None):
        """
        Unbans a specific user from the voice channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description=f"Please specify a user to unbanned",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            member_list = [mem.id for mem in channel.members]
            if member.id not in member_list:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            overwrite = channel.overwrites_for(member)
            overwrite.connect = True
            await channel.set_permissions(member, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description=f'{member.mention} has been unbanned from your channel',
                color=discord.Color.purple(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-kick',
        aliases=['v-kickuser']
    )
    async def _kick(self, ctx: commands.Context, member: discord.Member=None):
        """
        Kicks a specific user out of the voice channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description=f"Please specify a user to kicked",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            member_list = [mem.id for mem in channel.members]
            if member.id not in member_list:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            await member.move_to(None)
            done = discord.Embed(
                title='',
                description=f'{member.mention} has been kicked from your channel',
                color=discord.Color.purple(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-votekick',
        aliases=['v-vkick']
    )
    async def vkick(self, ctx: commands.Context, member: discord.Member=None):
        """
        Creates a vote kick for mentioned user.
        Every user in the voice channel can take part in the voting.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description=f"Please specify a user to vote kicked",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            member_list = [mem.id for mem in channel.members]
            if member.id not in member_list:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            else:
                voting = VoiceVoteManager(ctx)
                await voting.start_votekick(
                    member,
                    channel,
                    15
                )
    
    @commands.command(
        name='v-voteban',
        aliases=['v-vban']
    )
    async def _vban(self, ctx: commands.Context, member: discord.Member=None):
        """
        Creates a vote kick for mentioned user.
        Every user in the voice channel can take part in the voting.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description=f"Please specify a user to vote banned",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            member_list = [mem.id for mem in channel.members]
            if member.id not in member_list:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            else:
                voting = VoiceVoteManager(ctx)
                await voting.start_voteban(
                    member,
                    channel,
                    15
                )
    
    @commands.command(
        name='v-claim'
    )
    async def _claim(self, ctx: commands.Context):
        """
        Allows you to claim the channel if the initial owner leave the channel.
        """
        x = False
        voice_state = ctx.author.voice
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            data = saved.find_one({
                'channelID': channel.id
            })
            if data is None:
                fail = discord.Embed(
                    title='',
                    description=f"You don't own a channel!",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=fail)
            else:
                list_id = [member.id for member in channel.members]
                if data['authorID'] in list_id:
                    owner = ctx.guild.get_member(data['authorID'])
                    failed = discord.Embed(
                        title='',
                        description=f'{channel.mention} owner is still connected!!\nCurrent owner: {owner.mention}',
                        color=discord.Color.red(),
                        timestamp=ctx.message.created_at
                    )
                    await ctx.send(embed=failed)
                    x = True
            if x == False:
                saved.update_one({'channelID': channel.id}, {'$set': {'authorID': ctx.author.id}}, upsert=True)
                done = discord.Embed(
                    title='',
                    description=f'{channel.mention} owner has been changed to {ctx.author.mention}',
                    color=discord.Color.green(),
                    timestamp=ctx.message.created_at
                )
                await ctx.send(embed=done)
    
    @commands.command(
        name='v-transfer',
        aliases=['v-changeowner']
    )
    async def _transfer(self, ctx: commands.Context, member: discord.Member=None):
        """
        Transfer the channel ownership to mentioned member.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description='Please specify a user to transfer ownership'
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            member_list = [mem.id for mem in channel.members]
            if member.id not in member_list:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            saved.update_one({'channelID': channel.id}, {'$set': {'authorID': member.id}}, upsert=True)
            done = discord.Embed(
                title='',
                description=f'Transfer ownership succesfully!\nNew owner: {member.mention}',
                color=discord.Color.green()
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-mute',
        aliases=['v-muteuser']
    )
    async def _mute(self, ctx: commands.Context, member: discord.Member=None):
        """
        Mutes a specific user from the voice channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description=f"Please specify a user to mute",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            member_list = [mem.id for mem in channel.members]
            if member.id not in member_list:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            await member.edit(mute=True)
            done = discord.Embed(
                title='',
                description=f'{member.mention} has been muted',
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-unmute',
        aliases=['v-unmuteuser']
    )
    async def _unmute(self, ctx: commands.Context, member: discord.Member=None):
        """
        Unmutes a specific user from the voice channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description=f"Please specify a user to unmute",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            member_list = [mem.id for mem in channel.members]
            if member.id not in member_list:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            await member.edit(mute=False)
            done = discord.Embed(
                title='',
                description=f'{member.mention} has been unmuted',
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-hide',
        aliases=['v-invisible', 'v-close', 'v-invis']
    )
    async def _hide(self, ctx: commands.Context):
        """
        Makes your channel no longer visible for other users.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.view_channel = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description='Your channel now is invisible.',
                color=discord.Color.purple(),
                timestamp=ctx.message.created_at
            )
            await ctx.message.delete()
            await ctx.author.send(embed=done)
    
    @commands.command(
        name='v-unhide',
        aliases=['v-visible', 'v-open', 'v-visb']
    )
    async def _unhide(self, ctx: commands.Context):
        """
        Makes your channel no longer invisible for other users.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.view_channel = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description='Your channel now is visible.',
                color=discord.Color.purple(),
                timestamp=ctx.message.created_at
            )
            await ctx.message.delete()
            await ctx.author.send(embed=done)
    
    @commands.command(
        name='v-game',
        aliases=['v-setgame']
    )
    async def _game(self, ctx: commands.Context):
        """
        Updates the channels name to the name of the game you're currently playing.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            if isinstance(ctx.author.activity.type, discord.ActivityType.playing):
                vc_id = voice_state.channel
                channel = self.client.get_channel(vc_id)
                activity_name = ctx.author.activity.name
                await channel.edit(name=activity_name)
                saved.update_one({'authorID': ctx.author.id}, {'$set': {'channelName': activity_name}}, upsert=True)
                done = discord.Embed(
                    title='',
                    description=f"(Game Mode Enabled) Channel name has been changed to `{name}`",
                    color=discord.Color.green(),
                    timestamp=ctx.message.created_at
                )
                await ctx.send(embed=done)
            else:
                failed = discord.Embed(
                    title='',
                    description="You're currently not playing game!",
                    color=discord.Color.red()
                )
                await ctx.send(embed=failed)
    
    @commands.command(
        name='v-pushtotalk_on',
        aliases=['v-setpushtotalk', 'v-ptt_on']
    )
    async def _pushtotalk_on(self, ctx: commands.Context):
        """
        Turn on a Push To Talk mode for the voice channels.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.use_voice_activation = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description='Your channel now only for `Push to Talk` user',
                color=discord.Color.green()
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-pushtotalk_off',
        aliases=['v-nonpushtotalk', 'v-ptt_off']
    )
    async def _pushtotalk_off(self, ctx: commands.Context):
        """
        Turn off a Push To Talk mode for the voice channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.use_voice_activation = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description='Your channel now can be used for everyone',
                color=discord.Color.green()
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-lock',
        aliases=['v-setlock']
    )
    async def _lock(self, ctx: commands.Context):
        """
        Locks the voice channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.connect = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            done = discord.Embed(
                title="",
                description="Your channel now is locked",
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    #unlock
    @commands.command(
        name='v-unlock',
        aliases=['v-setunlock']
    )
    async def _unlock(self, ctx: commands.Context):
        """
        Unlocks the locked voice channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.connect = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            done = discord.Embed(
                title="",
                description="Your channel now is unlocked",
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-region',
        aliases=['v-reg', 'v-changeregion']
    )
    async def _region(self, ctx: commands.Context, *, region=None):
        """
        Modifies the channel region.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        region_list = [
            ['automatic', '1', 'auto'],
            ['brazil', '2', 'br'],
            ['europe', '3', 'eu'],
            ['hongkong', '4', 'hk'],
            ['india', '5', 'in'],
            ['japan', '6', 'jp'],
            ['russia', '7', 'ru'],
            ['singapore', '8', 'sg'],
            ['south africa', '9', 'south af'],
            ['south korea', '10', 'south kr'],
            ['sydney', '11', 'sny'],
            ['us central', '12', 'us_c'],
            ['us east', '13', 'us_e'],
            ['us south', '14', 'us_s'],
            ['us west', '15', 'us_w']
        ]
        region_list_cap = [
            'Automatic [1, auto]',
            'Brazil [2, br]',
            'Europe [3, eu]',
            'Hongkong [4, hk]',
            'India [5, in]',
            'Japan [6, jp]',
            'Russia [7, ru]',
            'Singapore [8, sg]',
            'South Africa [9 south afr]',
            'South Korea [10, south kr]',
            'Sydney [11, sny]',
            'US Central [12, us_c]',
            'US East [13, us_e]',
            'US South [14, us_s]',
            'US West [15, us_w]'
        ]
        if region is None:
            listed = "\n".join(region_list_cap)
            fail = discord.Embed(
                title='',
                description=f'Available Regions: `{listed}`',
                color=discord.Color.purple(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            msg = region.lower()
            if msg in region_list[0]:
                set_region = None
                replymsg = region_list_cap[0]
            elif msg in region_list[1]:
                set_region = VoiceRegion.brazil
                replymsg = region_list_cap[1]
            elif msg in region_list[2]:
                set_region = VoiceRegion.europe
                replymsg = region_list_cap[2]
            elif msg in region_list[3]:
                set_region = VoiceRegion.hongkong
                replymsg = region_list_cap[3]
            elif msg in region_list[4]:
                set_region = VoiceRegion.india
                replymsg = region_list_cap[4]
            elif msg in region_list[5]:
                set_region = VoiceRegion.japan
                replymsg = region_list_cap[5]
            elif msg in region_list[6]:
                set_region = VoiceRegion.russia
                replymsg = region_list_cap[6]
            elif msg in region_list[7]:
                set_region = VoiceRegion.singapore
                replymsg = region_list_cap[7]
            elif msg in region_list[8]:
                set_region = VoiceRegion.south_africa
                replymsg = region_list_cap[8]
            elif msg in region_list[9]:
                set_region = VoiceRegion.south_korea
                replymsg = region_list_cap[9]
            elif msg in region_list[10]:
                set_region = VoiceRegion.sydney
                replymsg = region_list_cap[10]
            elif msg in region_list[11]:
                set_region = VoiceRegion.us_central
                replymsg = region_list_cap[11]
            elif msg in region_list[12]:
                set_region = VoiceRegion.us_east
                replymsg = region_list_cap[12]
            elif msg in region_list[13]:
                set_region = VoiceRegion.us_south
                replymsg = region_list_cap[13]
            elif msg in region_list[14]:
                set_region = VoiceRegion.us_west
                replymsg = region_list_cap[14]
            else:
                set_region = None
                replymsg = region_list_cap[0]
            
            channel = voice_state.channel
            await channel.edit(rtc_region=set_region)
            done = discord.Embed(
                title='',
                description=f'Succesfully changed your channels region to {replymsg.capitalize()}',
                color=discord.Color.purple(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-bitrate',
        aliases=['v-setbitrate']
    )
    async def _bitrate(self, ctx: commands.Context, rate: int=None):
        """
        Modifies the channel bitrate.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            maxrate = 96
            if ctx.guild.premium_tier == 1:
                maxrate = 128
            elif ctx.guild.premium_tier == 2:
                maxrate = 256
            elif ctx.guild.premium_tier == 3:
                maxrate = 384
            
            if rate is None or not 7 < rate < maxrate+1:
                failed = discord.Embed(
                    title='',
                    description=f'Enter bitrate value: 8 - {str(maxrate)}',
                    color=discord.Color.purple(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            
            channel = voice_state.channel
            set_bitrate = round(rate * 1000)
            await channel.edit(bitrate=set_bitrate)
            saved.update_one({'authorID': ctx.author.id}, {'$set': {'channelBitrate': set_bitrate}}, upsert=True)
            done = discord.Embed(
                title='',
                description=f'Changed the channel bitrate to `{rate}Kbps`.',
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-whitelist',
        aliases=['v-allow', 'v-permit']
    )
    async def _whitelist(self, ctx: commands.Context, member: discord.Member=None):
        """
        Allows a certain user to join the channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description=f"Please specify a user to whitelist",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(member)
            overwrite.connect = True
            await channel.set_permissions(member, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description=f'{member.mention} has whitelisted to your voice channel',
                color=discord.Color.from_rgb(white['r'], white['g'], white['b']),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-blacklist',
        aliases=['v-deny', 'v-reject']
    )
    async def _blacklist(self, ctx: commands.Context, member: discord.Member=None):
        """
        Rejects a user from joining the channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if member is None:
            fail = discord.Embed(
                title='',
                description=f"Please specify a user to blacklist",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(member)
            overwrite.connect = False
            await channel.set_permissions(member, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description=f'{member.mention} has blacklisted from your voice channel',
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-save',
        aliases=['v-save_setting']
    )
    async def _save(self, ctx: commands.Context):
        """
        Saves the channel settings.
        Settings to save:
          - Channel name
          - Channel user limit
          - Channel bitrate
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            yes = ['y', 'yes']
            no = ['n', 'no']
            
            ch_name = data['channelName']
            ch_bitrate = data['channelBitrate']
            ch_userlimit = data['userLimit']
            embed = discord.Embed(
                title='Do you want save this settings?',
                description=f'Channel Information\nName: {ch_name}\nBitrate: {ch_bitrate}\nUser limit: {ch_userlimit}\n\n(y/n)\nTimeout: 30 seconds',
                color=discord.Color.purple()
            )
            await ctx.send(embed=embed)
            try
                response: discord.Message = await self.client.wait_for(
                    'message',
                    check=lambda m:m.author == ctx.author and m.channel == ctx.channel,
                    timeout=30
                )
            except asyncio.TimeoutError:
                fail = discord.Embed(
                    title='',
                    description='Timed out!!',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=fail)
            else:
                if response.content.lower() in yes:
                    saved.update_one({'authorID': ctx.author.id}, {'$set': {'keepSettings': 'true'}})
                    done = discord.Embed(
                        title='',
                        description='Settings saved',
                        color=discord.color.green(),
                        timestamp=ctx.message.created_at
                    )
                    await ctx.send(embed=done)
                elif response.content.lower() in no:
                    cancelled = discord.Embed(
                        title='',
                        description='Save settings cancelled',
                        color=discord.color.green(),
                        timestamp=ctx.message.created_at
                    )
                    await ctx.send(embed=cancelled)
                else:
                    failed = discord.Embed(
                        title='',
                        description='Invalid option!!',
                        color=discord.color.red(),
                        timestamp=ctx.message.created_at
                    )
                    await ctx.send(embed=failed)
    
    @commands.command(
        name='v-disablestream',
        aliases=['v-nonstream', 'v-rejectstream']
    )
    async def _disablestream(self, ctx: commands.Context):
        """
        Allows to disable Streaming mode for the channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.stream = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description='Stream/Screen share now is not allowed in your channel',
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-enablestream',
        aliases=['v-canstream', 'v-allowstream']
    )
    async def _enablestream(self, ctx: commands.Context):
        """
        Allows to enable Streaming mode for the channel.
        """
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        elif voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            channel = voice_state.channel
            overwrite = channel.overwrites_for(ctx.guild.default_role)
            overwrite.stream = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description='Stream/Screen share now is allowed in your channel',
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)

def setup(client: commands.Bot):
    client.add_cog(VoiceV2(client))
