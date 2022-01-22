import discord
from discord.ext import commands
from config import CONFIG
from pymongo import MongoClient

cluster = MongoClient(CONFIG['mongodb_url'])

levelling = cluster["database1"]

collection = levelling["level"]

class LevelSystem(commands.Cog):
    """LevelSystem related commands. """
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.guild.id == 836464932236165140:
            return
        author_id = message.author.id
        stats = collection.find_one({"_id": author_id})
        if not message.author.bot:
            if stats is None:
                newuser = {"_id": author_id, "xp": 100}
                collection.insert_one(newuser)
            else:
                xp = stats["xp"] + 5
                collection.update_one({"_id": author_id}, {"$set": {"xp": xp}})
                lvl = 0
                while True:
                    if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                        break
                    lvl += 1
                xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
                if xp == 0:
                    await message.channel.send(f"Well done {message.author.mention}! You leveled up to **Level: {lvl}**!")

    @commands.command()
    async def rank(self, ctx):
        """Show your Rank (Failed Program)"""
        if ctx.guild.id == 836464932236165140:
            return await ctx.send('Command has been disabled on this server!!')
        author_id = ctx.author.id
        stats = collection.find_one({"_id": author_id})
        if stats is None:
            embed = discord.Embed(description="You haven't sent any messages, no rank!!!")
            await ctx.channel.send(embed=embed)
        else:
            xp = stats["xp"]
            lvl = 0
            rank = 0
            while True:
                if xp < ((50 * (lvl ** 2)) + (50 * lvl)):
                    break
                lvl += 1
            xp -= ((50 * ((lvl - 1) ** 2)) + (50 * (lvl - 1)))
            boxes = int((xp / (200 * ((1 / 2) * lvl))) * 20)
            rankings = collection.find().sort("xp", -1)
            for x in rankings:
                rank += 1
                if stats["_id"] == x["_id"]:
                    break
                embed = discord.Embed(title="{}'s level stats".format(ctx.author.name))
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200 * ((1 / 2) * lvl))}", inline=True)
                embed.add_field(name="Rank", value=f"{rank}/{ctx.guild.member_count}", inline=True)
                embed.set_thumbnail(url=ctx.author.avatar_url)
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def leaderboard(self, ctx):
        """Show Leaderboard in Current Server"""
        if ctx.guild.id == 836464932236165140:
            return await ctx.send('Command has been disabled on this server!!')
        rankings = collection.find().sort("xp", -1)
        i = 1
        embed = discord.Embed(title="Rankings:")
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["_id"])
                tempxp = x["xp"]
                embed.add_field(name=f"{i}: {temp.name}", value=f"Total XP: {tempxp}", inline=False)
                i += 1
            except:
                 pass
            if i == 11:
                break
        await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(LevelSystem(client))
