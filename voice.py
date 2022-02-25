import discord
from discord.ext import commands
from discord import VoiceRegion
from pymongo import MongoClient
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

#REMAKE VOICEMASTER
class VoiceV2(commands.Cog):
    def __init__(self, client): 
        self.client = client
    
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        data = saved.find_one({
            'guildID': member.guild.id
        })
        
        guildSettings = saved_guild.find_one({
            'guildID': member.guild.id,
            'ownerID': member.guild.owner.id
        })
        if guildSettings is None:
            pass
        else:
            voiceID = guildSettings['voiceID']
            
            if after.channel.id == voiceID:
                categoryID = guildSettings['categoryID']
                
                name = f"{member.name}'s Channel"
                bitrate = 64000
                limit = 0
                
                category = self.client.get_channel(categoryID)
                channel2 = await member.guild.create_voice_channel(name, category=category)
                await member.move_to(channel2)
                await channel2.set_permissions(self.client.user, connect=True, read_messages=True)
                await channel2.edit(name=name, user_limit=limit, bitrate=bitrate)
                saved.insert_one({
                    'guildID': member.guild.id,
                    'authorID': member.id,
                    'channelID': channel2.id
                })
                def check(a,b,c):
                    return len(channel2.members) == 0
                await self.client.wait_for('voice_state_update', check=check)
                await channel2.delete()
                await asyncio.sleep(5)
                saved.delete_one({
                    'authorID': member.id
                })
    
    @commands.command(
        name='v-fetch_id',
        aliases=['v-get_id']
    )
    @commands.has_permissions(
        manage_guild=True
    )
    async def fetch_id(self, ctx, *, channel: discord.VoiceChannel=None):
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
        manage_guild=True
    )
    async def _setup(self, ctx):
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
            if get_cat.type != discord.ChannelType.category:
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
                    if get_ch.type != discord.ChannelType.voice:
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
    async def _userlimit(self, ctx, limit: int=None):
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
            await channel.edit(user_limit=limit)
            saved.update_one({'authorID': ctx.author.id}, {'$set': {'userLimit': limit}}, upsert=True)
            if limit <= 1:
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
    async def _name(self, ctx, *, name):
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
            await channel.edit(name=name)
            saved.update_one({'authorID': ctx.author.id}, {'$set': {'channelName': name}}, upsert=True)
            done = discord.Embed(
                title='',
                description=f"Channel name has been changed to `{name}`",
                color=discord.Color.green(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-ban',
        aliases=['v-banuser']
    )
    async def _ban(self, ctx, member: discord.Member=None):
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
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
            if member not in channel.members:
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
            overwrite.read_messages = True
            await channel.set_permissions(member, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description=f'{member.mention} has been banned from your channel',
                color=discord.Color.purple(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-kick',
        aliases=['v-kickuser']
    )
    async def _kick(self, ctx, member: discord.Member=None):
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
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def vkick(self, ctx, member: discord.Member=None):
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
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
            if member not in channel.members:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            else:
                member_id = [members.id for members in channel.members]
                yes = 0
                no = len(channel.members) - yes
                voting = discord.Embed(
                    title='--- Vote Kick ---',
                    description=f'Waiting vote to kick {member.mention}\n15 Seconds from now\nNot Voting: **No**\nCurrent member can vote in {channel.mention}: {len(channel.members)}',
                    color=discord.Color.blurple()
                )
                vote = await ctx.send(embed=voting)
                await vote.add_reaction('✔️')
                try:
                    react_count = await self.client.wait_for(
                          'raw_reaction_add',
                          check=lambda payload:payload.emoji ==  '✔️' and payload.message_id == vote.id and payload.channel_id == ctx.channel.id,
                          timeout=15
                    )
                    if react_count.member.id not in member_id:
                        return
                    if react_count:
                        yes += 1
                except asyncio.TimeoutError:
                    done = discord.Embed(
                        title='',
                        description='Voting is Done!!\nCounting result...',
                        color=discord.Color.purple()
                    )
                    await ctx.send(embed=done)
                else:
                    raw_res = discord.Embed(
                        title='--- Vote Result ---',
                        description=f'Yes: {yes}\nNo: {no}',
                        color=discord.Color.purple()
                    )
                    await ctx.send(embed=raw_res)
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
                    await ctx.send(embed=result)
    
    @commands.command(
        name='v-claim'
    )
    async def _claim(self, ctx):
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
            data = saved.find_one({
                'channelID': voice_state.channel.id
            })
            channel = voice_state.channel
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
    async def _transfer(self, ctx, member: discord.Member=None):
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
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
            if member not in channel.members:
                fail = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=fail)
            saved.update_one({'channelID': channel.id}, {'$set': {'authorID': member.id}}, upsert=True)
            done = discord.Embed(
                title='',
                description=f'Transfer ownership succesfull!\nNew owner: {member.mention}',
                color=discord.Color.green()
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-mute',
        aliases=['v-muteuser']
    )
    async def _mute(self, ctx, member: discord.Member=None):
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
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
            if member not in channel.members:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            overwrite = channel.overwrites_for(member)
            overwrite.speak = False
            await channel.set_permissions(member, overwrite=overwrite)
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
    async def _unmute(self, ctx, member: discord.Member=None):
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
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
            if member not in channel.members:
                failed = discord.Embed(
                    title='',
                    description=f'{member.mention} currently not in your channel',
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            overwrite = channel.overwrites_for(member)
            overwrite.speak = True
            await channel.set_permissions(member, overwrite=overwrite)
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
    async def _hide(self, ctx):
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def _unhide(self, ctx):
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def _game(self, ctx):
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            if ctx.author.activity.type == discord.ActivityType.playing:
                vc_id = data['channelID']
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
        aliases=['v-setpushtotalk', 'v-ptt']
    )
    async def _pushtotalk_on(self, ctx):
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
        aliases=['v-nonpushtotalk', 'v-nonptt']
    )
    async def _pushtotalk_off(self, ctx):
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def _lock(self, ctx):
        """Lock Current Voice Channel"""
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def _unlock(self, ctx):
        """Unlock Current Locked Voice Channel (Failed Program)"""
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def _region(self, ctx, *, region=None):
        data = saved.find_one({
            'authorID': ctx.author.id
        })
        voice_state = ctx.author.voice
        region_list = [
            'automatic',
            'brazil',
            'europe',
            'hongkong',
            'india',
            'japan',
            'russia',
            'singapore',
            'south africa',
            'south korea',
            'sydney',
            'us central',
            'us east',
            'us south',
            'us west'
        ]
        region_list_cap = [
            'Automatic',
            'Brazil',
            'Europe',
            'Hongkong',
            'India',
            'Japan',
            'Russia',
            'Singapore',
            'South Africa',
            'South Korea',
            'Sydney',
            'US Central',
            'US East',
            'US South',
            'US West'
        ]
        if region is None:
            listed = ", ".join(region_list_cap)
            fail = discord.Embed(
                title='',
                description=f'Available Regions: `{listed}`',
                color=discord.Color.purple(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            msg = region.lower()
            if msg == region_list[0]:
                set_region = None
                replymsg = region_list[0]
            elif msg == region_list[1]:
                set_region = VoiceRegion.brazil
                replymsg = region_list[1]
            elif msg == region_list[2]:
                set_region = VoiceRegion.europe
                replymsg = region_list[2]
            elif msg == region_list[3]:
                set_region = VoiceRegion.hongkong
                replymsg = region_list[3]
            elif msg == region_list[4]:
                set_region = VoiceRegion.india
                replymsg = region_list[4]
            elif msg == region_list[5]:
                set_region = VoiceRegion.japan
                replymsg = region_list[5]
            elif msg == region_list[6]:
                set_region = VoiceRegion.russia
                replymsg = region_list[6]
            elif msg == region_list[7]:
                set_region = VoiceRegion.singapore
                replymsg = region_list[7]
            elif msg == region_list[8]:
                set_region = VoiceRegion.south_africa
                replymsg = region_list[8]
            elif msg == region_list[9]:
                set_region = VoiceRegion.south_korea
                replymsg = region_list[9]
            elif msg == region_list[10]:
                set_region = VoiceRegion.sydney
                replymsg = region_list[10]
            elif msg == region_list[11]:
                set_region = VoiceRegion.us_central
                replymsg = region_list[11]
            elif msg == region_list[12]:
                set_region = VoiceRegion.us_east
                replymsg = region_list[12]
            elif msg == region_list[13]:
                set_region = VoiceRegion.us_south
                replymsg = region_list[13]
            elif msg == region_list[14]:
                set_region = VoiceRegion.us_west
                replymsg = region_list[14]
            else:
                set_region = None
                replymsg = region_list[0]
            
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def _bitrate(self, ctx, rate: int=None):
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
        if voice_state is None:
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
            
            if not 7 < rate < maxrate+1:
                failed = discord.Embed(
                    title='',
                    description=f'Enter bitrate value: 8 - {str(maxrate)}',
                    color=discord.Color.purple(),
                    timestamp=ctx.message.created_at
                )
                return await ctx.send(embed=failed)
            
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def _whitelist(self, ctx, member: discord.Member=None):
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
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def _blacklist(self, ctx, member: discord.Member=None):
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
        if data is None:
            fail = discord.Embed(
                title='',
                description=f"You don't own a channel!",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
            overwrite = channel.overwrites_for(member)
            overwrite.connect = False
            overwrite.read_messages = True
            await channel.set_permissions(member, overwrite=overwrite)
            done = discord.Embed(
                title='',
                description=f'{member.mention} has blacklisted from your voice channel',
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            await ctx.send(embed=done)
    
    @commands.command(
        name='v-disablestream',
        aliases=['v-nonstream', 'v-justaudio']
    )
    async def _disablestream(self, ctx):
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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
    async def _enablestream(self, ctx):
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
        if voice_state is None:
            fail = discord.Embed(
                title='',
                description="You're not in voice channel. Please use this command in voice channel.",
                color=discord.Color.red(),
                timestamp=ctx.message.created_at
            )
            return await ctx.send(embed=fail)
        else:
            vc_id = data['channelID']
            channel = self.client.get_channel(vc_id)
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

def setup(client):
    client.add_cog(VoiceV2(client))
