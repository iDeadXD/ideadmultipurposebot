import discord
from discord.ext import commands
from datetime import datetime
from pymongo import MongoClient
from config import CONFIG

dataclient = MongoClient(CONFIG['mongodb_url'])
database = dataclient['database4']
saved = database['msgchannel']

class Setup(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def setchannelhere(self, ctx, types: str=None):
        ch_data = saved.find_one({'_id': ctx.guild.id})
        
        if types is None:
            fail = discord.Embed(title="" ,description="Available type: ```join/leave```", color=discord.Color.red())
            return await ctx.send(embed=fail)
        else:
            try:
                if str(types) == 'join':
                    if ch_data is None:
                        new_data = {'_id': ctx.guild.id, 'welcome_ch': ctx.channel.id}
                        saved.insert_one(new_data)
                        done = discord.Embed(
                            title="",
                            description=f"Welcome Channel has been set to ```{ctx.channel.name}```",
                            color=discord.Color.blurple()
                        )
                        await ctx.send(embed=done)
                    else:
                        saved.update_one({'_id': ctx.guild.id}, {'$set': {'welcome_ch': ctx.channel.id}})
                        done = discord.Embed(
                            title="",
                            description=f"Welcome Channel has been updated to ```{ctx.channel.name}```",
                            color=discord.Color.purple()
                        )
                        await ctx.send(embed=done)
                elif str(types) == 'leave':
                    if ch_data is None:
                        new_data = {'_id': ctx.guild.id, 'leave_ch': ctx.channel.id}
                        saved.insert_one(new_data)
                        done = discord.Embed(
                            title="",
                            description=f"Leave Channel has been set to ```{ctx.guild.name}```",
                            color=discord.Color.blurple()
                        )
                        await ctx.send(embed=done)
                    else:
                        saved.update_one({'_id': ctx.guild.id}, {'$set': {'leave_ch': ctx.channel.id}})
                        done = discord.Embed(
                            title="",
                            description=f"Leave Channel has been updated to ```{ctx.channel.name}```",
                            color=discord.Color.purple()
                        )
                        await ctx.send(embed=done)
                else:
                    failed = discord.Embed(
                        title="",
                        description="Invalid Options. Command Ignored!!",
                        color=discord.Color.red()
                    )
                    await ctx.send(embed=failed)
            except Exception as e:
                return print(e)

def setup(client):
    client.add_cog(Setup(client))
