import discord
from discord.ext import commands

class Premium(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.premium = [
            843132313562513408
        ]
    
    @commands.command()
    async def test(self, ctx):
        if ctx.author.id in self.premium:
             await ctx.reply('Anda sudah premium.')
        else:
             await ctx.send('Anda belum premium.')

def setup(client):
    client.add_cog(Premium(client))
