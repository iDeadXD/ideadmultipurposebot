import discord
from discord.ext import commands
from pymongo import MongoClient

class Guilds(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    def cog_check(ctx):
        if ctx.guild.id == 840594344939356181:
            return print('Disabled for Now')
    
    @commands.command()
    async def boostcount(self, ctx):
        booster = [m.mention for m in ctx.guild.premium_subscribers]
        
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
        boosted.add_field(name="List of Booster", value="\n".join(booster))
        boosted.set_footer(text="Thanks for boost this server")
        
        await ctx.send(embed=boosted)

def setup(client):
    client.add_cog(Guilds(client))
