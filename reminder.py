import discord
from discord.ext import commands, tasks
import asyncio
from pymongo import MongoClient
from config import CONFIG
from datetime import datetime, timedelta

dataclient = MongoClient(CONFIG['mongodb_url'])
database = dataclient['database5']
collection = database['reminder']

class Reminder(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.reminder_task.start()

    def cog_unload(self):
        self.reminder_task.cancel()

    @tasks.loop(minutes=1.0)
    async def reminder_task(self):
        data = collection.find_one({})
        # async for i in data:
        for reminder in data:
            now = datetime.now()
            remindme = str({reminder['time']})
            remind = datetime.strptime(remindme, "%Y-%m-%d %H:%M:%S.%f")
            if now >= remind:
                guild = self.client.get_guild(remind['guild_id'])
                member = guild.get_member(remind['_id'])
                await member.send(f"Reminder: `{remind['msg']}`")

    @commands.command()
    async def remindme(self, ctx, time, *, reminder):
        time_conversion = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}
        remindseconds = int(time[0]) * time_conversion[time[-1]]
        remindertime = datetime.now() + timedelta(seconds=remindseconds)
        author_id = ctx.author.id
        guild_id = ctx.guild.id
        if ctx.author.bot:
            return

        rem_info = {"_id": author_id, "guild_id": guild_id, "time": remindertime, "msg": reminder}

        collection.insert_one(rem_info)
        await ctx.send('Reminder was set!')


def setup(client):
    client.add_cog(Reminder(client))
