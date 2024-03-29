import discord
from discord.ext import commands
import random
import sys
import asyncio

#Games Class
class Games(commands.Cog):
    """Simple Games related Commands"""
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def rng(self, ctx):
        try:
            num = random.randint(1, sys.maxsize)
            
            waits = discord.Embed(
                title="",
                description="Enter your number.",
                color=discord.Color.purple()
            )
            
            await ctx.send(embed=waits)
            count = await self.client.wait_for('message', check=lambda message:message.author == ctx.author and message.channel == ctx.channel, timeout=10)
            
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
        except asyncio.TimeoutError:
            failed = discord.Embed(
                title="",
                description="Game Timeout",
                color=discord.Color.red()
            )
            return await ctx.send(embed=failed)
    
    @commands.command()
    async def rps(self, ctx):
        try:
            types = ["rock", "paper", "scissor"]
               
            bots = random.choice(types)
              
            await ctx.send("rock/paper/scissor")
            response = await self.client.wait_for('message', check=lambda message:message.author == ctx.author and message.channel == ctx.channel, timeout=10)
            msg = response.content.lower()
            
            if msg == 'rock':
                if str(bots) == 'scissor':
                    await ctx.send(bots)
                    await ctx.send("You win")
                elif str(bots) == 'paper':
                    await ctx.send(bots)
                    await ctx.send("Bots Win")
                elif str(bots) == 'rock':
                    await ctx.send(bots)
                    await ctx.send("Draw")
            if msg == 'paper':
                if str(bots) == 'rock':
                    await ctx.send(bots)
                    await ctx.send("You win")
                elif str(bots) == 'scissor':
                    await ctx.send(bots)
                    await ctx.send("Bots Win")
                elif str(bots) == 'paper':
                    await ctx.send(bots)
                    await ctx.send("Draw")
            if msg == 'scissor':
                if str(bots) == 'paper':
                    await ctx.send(bots)
                    await ctx.send("You win")
                elif str(bots) == 'rock':
                    await ctx.send(bots)
                    await ctx.send("Bots Win")
                elif str(bots) == 'scissor':
                    await ctx.send(bots)
                    await ctx.send("Draw")
            else:
                return #some code
        except asyncio.TimeoutError:
            failed = discord.Embed(
                title="",
                description="Game Timeout",
                color=discord.Color.red()
            )
            return await ctx.send(embed=failed)

def setup(client):
    client.add_cog(Games(client))
