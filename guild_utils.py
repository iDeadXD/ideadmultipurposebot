import discord
from discord.ext import commands
from pymongo import MongoClient

class Guilds(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def boostcount(self, ctx):
        booster = len(ctx.guild.premium_subscribers)
        
        if booster == 0:
            no_boost = discord.Embed(
                title="",
                description="There are no members who boost this server. Do not be sad",
                color=discord.Color.purple()
            )
            return await ctx.send(embed=no_boost)
        
        boosted = discord.Embed(
            title="--- Server Booster ---",
            color=discord.Color.magenta()
        )
        boosted.set_thumbnail(url=ctx.guild.icon_url)
        boosted.add_field(name="Booster Count", value=f"{str(ctx.guild.premium_subscription_count)}")
        boosted.add_field(name="List of Booster", value=", ".join(booster.name))
        boosted.set_footer(text="Thanks for boost this server")
        
        await ctx.send(embed=boosted)
    
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def prefix(self, ctx, prefixs=None):
        if prefixs is None:
            fail =discord.Embed(
                title="",
                description="Enter your prefix to change the default prefix. Default Prefix: >",
                color=discord.Color.green()
            )
            await ctx.send(embed=fail)
        
        data = await self.client.collection.find(ctx.guild.id)
        if data is None or "prefixes" not in data:
            data = {"guild_id": ctx.guild.id, "_prefix": prefixs}
        data["_prefix"] = prefixs
        await self.client.collection.upsert(data)
        
        done = discord.Embed(
            title="",
            description=f"{self.client.user.mention}'s Prefix has been set to {prefixs}",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=done)
    
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def deleteprefix(self, ctx):
        await self.client.collection.unset({"guild_id": ctx.guild.id, "_prefix": 1})
        
        done = discord.Embed(
            title="",
            description=f"{self.client.user.mention}'s Prefix has been set to default ( > )",
            color=discord.Color.green()
        )
        
        await ctx.send(embed=done)

def setup(client):
    client.add_cog(Guilds(client))
