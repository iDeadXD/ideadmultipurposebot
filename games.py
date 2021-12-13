import discord
from discord.ext import commands
import random
import asyncio

class Games(commands.Cog):
    """Simple Games related Commands"""
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def rng(self, ctx):
        
        num = random.randint(1, 100000)
        
        waits = discord.Embed(
            title="",
            description="Enter your number. Range: 1 - 100000",
            color=discord.Color.purple()
        )
        
        await ctx.send(embed=waits)
        count = await self.client.wait_for('message', check=lambda message:message.author == ctx.author and message.channel == ctx.channel, timeout=10)
        
        if not 0 < int(count.content) < 100001:
            return await ctx.send("Enter number range: 1 - 100000")
        else:
            try:
                if num < int(count.content):
                    win = discord.Embed(
                        title="--- RNG Games ---",
                        description=f"Congratulation. You Win, {ctx.message.author.mention}",
                        color=discord.Color.purple()
                    )
                    win.add_field(name="Your Number", value=f"{str(count.content)}")
                    win.add_field(name="Bot Number", value=str(num))
                        
                    await ctx.send(embed=win)
                if num > int(count.content):
                    lose = discord.Embed(
                        title="--- RNG Games ---",
                        description=f"Oh no. You lose, {ctx.message.author.mention}",
                        color=discord.Color.red()
                    )
                    lose.add_field(name="Your Number", value=f"{str(count.content)}")
                    lose.add_field(name="Bot Number", value=str(num))
                        
                    await ctx.send(embed=lose)
            except asyncio.exceptions.TimeoutError():
                return await ctx.send("Games Timed out. (Timeout: 10 seconds)")

def setup(client):
    client.add_cog(Games(client))