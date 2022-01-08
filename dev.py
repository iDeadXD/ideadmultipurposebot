import discord
from discord.ext import commands
import asyncio

class Developer(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        
        try:
            getpass = discord.Embed(
                title="",
                description="Are you sure want shutdown me? (Enter Password)",
                color=ctx.author.color
            )
            sendconfirm = await ctx.send(embed=getpass)
            
            passw = await self.client.wait_for('message', check=lambda message:message.author == ctx.author and message.channel == ctx.channel, timeout=10)
            
            if passw.content == 'idead1511':
                await sendconfirm.delete()
                await passw.delete()
                await asyncio.sleep(1)
                await ctx.send("Shutting Down...")
                await asyncio.sleep(4)
                await ctx.send("Shutdown Completed.")
                await asyncio.sleep(1)
                await self.client.close()
            else:
                await ctx.send("Wrong Password!!")
        except asyncio.TimeoutError:
            failed = discord.Embed(
                title="",
                description="Timed Out!!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=failed)
        except commands.NotOwner:
            failed = discord.Embed(
                title="",
                description="You're not owner of this bot!!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=failed)

def setup(client):
    client.add_cog(Developer(client))
