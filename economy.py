import discord
from discord.ext import commands
from pymongo import MongoClient
import asyncio
import random
from config import CONFIG

class Economy(commands.Cog):
    
    def __init__(self, client):
        self.client = client
    
    database = MongoClient(CONFIG['mongodb_url'])
    bank = database['database3']
    balance = bank['balance']
    
    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def claim(self, ctx):
        data = balance.find_one({'_id': ctx.message.author.id})
        
        if data is None:
            new_data = {"_id": ctx.message.author.id, "money": 500, "status": "Account Registered"}
            done = discord.Embed(
                title="--- Daily Claim ---",
                description="Since you are claiming for the first time, you got 500 free",
                color=discord.Color.purple()
            )
            balance.insert_one(new_data)
            await ctx.send(embed=done)
        else:
            daily = random.randint(200, 1000)
            updated = data['money'] + int(daily)
            balance.update_one({"_id": ctx.message.author.id}, {"$set": {"money": daily}}, {"$set": {"status": f"{str(daily)} claimed from Daily Claim"}})
            done = discord.Embed(
                title="--- Daily Claim ---",
                description=f"You got {str(daily)} for daily claim today. Daily Claim cooldown: 24 hours",
                color=discord.Color.purple()
            )
            await ctx.send(embed=done)
    
    @claim.error
    async def claim_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="You're on a cooldown!", color=discord.Color.blue())
    
            cd = round(error.retry_after)
            hours = str(cd // 3600)
            minutes = str(cd % 60)
    
            embed.add_field(
                name="\u200b",
                value=
                f"Do you want free money?\n Wait for ```{hours}``` hours ```{minutes}``` minutes"
            )
            await ctx.send(embed=embed)
        else:
            raise error
    
    @commands.command(alliases=["give", "tf"])
    @commands.cooldown(5, 86400, commands.BucketType.user)
    async def transfer(self, ctx, member: discord.Member=None, amount: int=None, *, reason=None):
        
        if member is None or amount is None:
            fail1 = discord.Embed(
                title="",
                description="Transfer money to whoever you want to give. Example: ```>transfer @iDead#0000 50000 reason(Optional)```",
                color=discord.Color.red()
            )
            return await ctx.send(embed=fail1)
        else:
            self_data = balance.find_one({"_id": ctx.message.author.id})
            recv_data = balance.find_one({"_id": member.id})
            
            if self_data is None or recv_data is None:
                fail2 = discord.Embed(
                    title="",
                    description="You or those you mention do not have a balance account. Make sure you or those you mention use the command ```>claim``` for account registration automatically",
                    color=discord.Color.red()
                )
                return await ctx.send(embed=fail2)
            if int(self_data['money']) == 0:
                fail3 = discord.Embed(
                    title="",
                    description="You have no money at all. You can earn money for free from Daily Claim",
                    color=discord.Color.red()
                )
                return await ctx.send(embed=fail3)
            else:
                try:
                    yes = ["y", "yes"]
                    no = ["n", "no"]
                    
                    confirm = discord.Embed(
                        title="",
                        description=f"Are you sure want to transfer {str(amount)} to {member.name + '#' + member.discriminator} ? (y/n) (Make sure to check your money first with ```>balance``` commands)",
                        color=discord.Color.purple()
                    )
                    await ctx.send(embed=confirm)
                    msg = await self.client.wait_for('message', check=lambda message : message.author == ctx.author and message.channel == ctx.channel, timeout=10)
                    
                    if msg.content in yes:
                        if self_data['money'] - amount != 0:
                            data1 = self_data['money'] - amount
                            data2 = recv_data['money'] + amount
                            
                            balance.update_one({"_id": ctx.message.author.id}, {"$set": {"money": data1}}, {"$set": {"status": f"Transfer {amount} to {member.name + '#' + member.discriminator}"}})
                            balance.update_one({"_id": member.id}, {"$set": {"money": data2}})
                            
                            done = discord.Embed(
                                title="--- Money Transfer ---",
                                description="Transfer Completed",
                                color=discord.Color.purple()
                            )
                            done.set_thumbnail(url=member.avatar_url)
                            done.add_field(name="From", value=f"{ctx.message.author.name + '#' + ctx.message.author.discriminator}")
                            done.add_field(name="Transfer to", value=f"{member.name + '#' + member.discriminator}")
                            done.add_field(name="Amount", value=f"{str(amount)}")
                            await ctx.send(embed=done)
                            await member.send(embed=done)
                            
                            if reason:
                                done.add_field(name="Reason", value=str(reason))
                                await ctx.send(embed=done)
                                await member.send(embed=done)
                        elif self_data['money'] - amount == 0:
                            data1 = self_data['money'] - amount
                            data2 = recv_data['money'] + amount
                            
                            balance.update_one({"_id": ctx.message.author.id}, {"$set": {"money": data1}}, {"$set": {"status": f"Transfer {amount} to {member.id}"}})
                            balance.update_one({"_id": member.id}, {"$set": {"money": data2}})
                            
                            done = discord.Embed(
                                title="--- Money Transfer ---",
                                description="Transfer All Completed",
                                color=discord.Color.purple()
                            )
                            done.set_thumbnail(url=member.avatar_url)
                            done.add_field(name="From", value=f"{ctx.message.author.name + '#' + ctx.message.author.discriminator}")
                            done.add_field(name="Transfer to", value=f"{member.name + '#' + member.discriminator}")
                            done.add_field(name="Amount", value=f"{str(amount)}")
                            await ctx.send(embed=done)
                            await member.send(embed=done)
                            
                            if reason:
                                done.add_field(name="Reason", value=str(reason))
                                await ctx.send(embed=done)
                                await member.send(embed=embed)
                        else:
                            fail4 = discord.Embed(
                                title="",
                                description="Transfer has failed",
                                color=discord.Color.red()
                            )
                            fail4.add_field(name="Reason", value="You cannot transfer more money than your current amount (Check your money with ```>balance``` commands)")
                            await ctx.send(embed=fail4)
                    elif msg.content in no:
                        cancelled = discord.Embed(
                            title="",
                            description="Transfer cancelled!!",
                            color=discord.Color.green()
                        )
                        await ctx.send(embed=cancelled)
                    else:
                        cancelled = discord.Embed(
                            title="",
                            description="Transfer cancelled!!",
                            color=discord.Color.green()
                        )
                        await ctx.send(embed=cancelled)
                except TimeoutError:
                    failed = discord.Embed(
                        title="",
                        description="Confirmation Timed out",
                        color=discord.Color.red()
                    )
                    return await ctx.send(embed=failed)
    
    @transfer.error
    async def transfer_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(
                title="You're on a cooldown!", color=discord.Color.blue())
    
            cd = round(error.retry_after)
            hours = str(cd // 3600)
            minutes = str(cd % 60)
    
            embed.add_field(
                name="\u200b",
                value=
                f"You can only transfer money 5 times a day\n Wait for ```{hours}``` hours ```{minutes}``` minutes"
            )
            await ctx.send(embed=embed)
        else:
            raise error
    
    @commands.command()
    async def buy(self, ctx):
        fail = discord.Embed(
            title="",
            description="For now, this command is still under development (Can not be used)!!",
            color=discord.Color.green()
        )
        await ctx.send(embed=fail)
    
    @commands.command(alliases=["bal", "bl"])
    async def balance(self, ctx):
        data = balance.find({'_id': ctx.message.author.id})
        
        if data is None:
            fail = discord.Embed(
                title="",
                description="Please claim daily rewards for the first time. Use ```>claim``` command",
                color=discord.Color.green()
            )
            return await ctx.send(embed=fail)
        else:
            for curr_data in data:
                money_data = curr_data['money']
                status = curr_data['status']
            
            curr_status = "No activity" if str(status) is None else str(status)
            
            done = discord.Embed(
                title="--- Current Balance ---",
                description=f"{ctx.message.author.name}'s Balance",
                color=discord.Color.purple()
            )
            done.add_field(name="\u200b", value=f"Your Current Balance: {str(money_data)}")
            done.add_field(name="\u200b", value=f"Last Activity: {str(curr_status)}")
            
            await ctx.send(embed=done)

def setup(client):
    client.add_cog(Economy(client))
