import discord
from discord.ext import commands
import asyncio

class Developer(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    @commands.is_owner()
    async def shutdown(self, ctx):
        if ctx.author.id != 843132313562513408:
            return await ctx.send("You're not owner of this bot!")
        
        try:
            getpass = discord.Embed(
                title="",
                description="Are you sure want shutdown me? (Enter Password)",
                color=ctx.author.color
            )
            await ctx.send(embed=getpass)
            
            passw = await self.client.wait_for('message', check=lambda message:message.author == ctx.author and message.channel == ctx.channel, timeout=60)
            
            if passw.content == 'idead1511':
                await passw.delete()
                for guild in len(self.client.guilds):
                    for owner in len(guild.owner):
                        await owner.send("I'm Offline Now (This message is automatically sent when the bot is shutting down.)")
                await asyncio.sleep(1)
                await ctx.send("Shutting Down...")
                await asyncio.sleep(3)
                await ctx.send("Shutdown Completed.")
                await asyncio.sleep(1)
                await self.client.logout()
            else:
                await ctx.send("Wrong Password!!")
        except asyncio.TimeoutError:
            failed = discord.Embed(
                title="",
                description="Timed Out!!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=failed)

def setup(client):
    client.add_cog(Developer(client))
