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
            await ctx.send(embed=getpass)
            
            passw = self.client.wait_for('message', check=lambda message:message.author == ctx.author and message.channel == ctx.channel, timeout=60)
            
            if passw.content == '<yourpass>':
                for guild in self.client.guilds:
                    for owner in guild.owner:
                        await owner.send("I'm Offline Now (This message is automatically sent when the bot is shutting down.)")
                await asyncio.sleep(1)
                await ctx.send("Shutting Down...")
                await asyncio.sleep(3)
                await ctx.send("Shutdown Completed.")
                await asyncio.sleep(1)
                await self.client.logout()
            else:
                await ctx.send("Wrong Password!!")
        except:
            failed = discord.Embed(
                title="",
                description="You're not owner of this bot!!",
                color=discord.Color.red()
            )
            return await ctx.send(embed=failed)

def setup(client):
    client.add_cog(Developer(client))
