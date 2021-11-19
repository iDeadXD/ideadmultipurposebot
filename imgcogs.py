import discord
from discord.ext import commands
import random
import time
import requests
import pytz
from datetime import datetime
from imgapi import SFW, NSFW, MEME
from custom_msg import W_MESSAGE, H_MESSAGE, B_MESSAGE, S_MESSAGE, M_MESSAGE, K_MESSAGE

class Image(commands.Cog):
    """Image Related Commands."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def waifu(ctx, member : discord.Member=None):
        """Waifu Image for You"""
        if member is None:
            member = ctx.author
        if ctx.channel.is_nsfw():
            await ctx.send('Note: Write this command outside the NSFW channel')
            return
        url = SFW['waifu1']
        r = requests.get(url)
        data = r.json()
        img_url = data['url']
        desc = [
            str(W_MESSAGE['w_msg1']).format(member.mention),
            str(W_MESSAGE['w_msg2']).format(member.mention),
            str(W_MESSAGE['w_msg3']).format(member.mention),
            str(W_MESSAGE['w_msg4']).format(member.mention),
            str(W_MESSAGE['w_msg5']).format(member.mention),
            str(W_MESSAGE['w_msg6']).format(member.mention),
            str(W_MESSAGE['w_msg7']).format(member.mention),
            str(W_MESSAGE['w_msg8']).format(member.mention),
            str(W_MESSAGE['w_msg9']).format(member.mention),
            str(W_MESSAGE['w_msg10']).format(member.mention)
        ]
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Random Waifu Image ---",
            description=random.choice(desc)
        )
        embed.set_image(url=img_url)
        embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
    
    @commands.command()
    async def hentai(ctx):
        """Hentai Anime Image (18+ Warning)"""
        if ctx.channel.is_nsfw():
            url1 = NSFW['hentai1']
            url2 = NSFW['hentai2']
            url3 = NSFW['hentai3']
            r1 = requests.get(url1)
            r2 = requests.get(url2)
            r3 = requests.get(url3)
            data1 = r1.json()
            data2 = r2.json()
            data3 = r3.json()
            img_url1 = data1['url']
            img_url2 = data2['url']
            img_url3 = data3['url']
            imgdata = [
                img_url1,
                img_url2,
                img_url3,
            ]
            desc = [
                str(H_MESSAGE['h_msg1']).format(ctx.message.author.mention),
                str(H_MESSAGE['h_msg2']).format(ctx.message.author.mention),
                str(H_MESSAGE['h_msg3']).format(ctx.message.author.mention),
                str(H_MESSAGE['h_msg4']).format(ctx.message.author.mention),
            ]
            embed = discord.Embed(
                color=discord.Color.green(),
                title="--- 18+ Hentai Image ---",
                description=random.choice(desc),
            )
            embed.set_image(url=random.choice(imgdata))
            embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
                
            await ctx.send(embed=embed)
        else:
            await ctx.send('Note: Write this command in NSFW channel')
    
    @commands.command()
    async def kiss(ctx, member : discord.Member=None):
        if member is None:
            await ctx.send("Note: No G*Y/Selfkiss!!! You must tag someone for your kiss partner")
            return
        url7 = SFW['kiss1']
        r7 = requests.get(url7)
        data7 = r7.json()
        imgdata = data7['url']
        desc = [
            str(K_MESSAGE['k_msg1']).format(ctx.message.author.mention, member.mention),
            str(K_MESSAGE['k_msg2']).format(ctx.message.author.mention, member.mention),
        ]
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Kiss for You ---",
            description=random.choice(desc)
        )
        
        embed.set_image(url=imgdata)
        embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def slap(ctx, member : discord.Member=None):
        """Slaps your friend or yourself"""
        if member is None:
            member = ctx.author
        url4 = SFW['slap1']
        r4 = requests.get(url4)
        data4 = r4.json()
        imgdata = data4['url']
        desc = [
            str(S_MESSAGE['s_msg1']).format(ctx.message.author.mention, member.mention),
            str(S_MESSAGE['s_msg2']).format(ctx.message.author.mention, member.mention),
        ]
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Slap Someone ---",
            description=random.choice(desc),
        )
        embed.set_image(url=imgdata)
        embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=embed)
    
    @commands.command()
    async def bonk(ctx, member : discord.Member=None):
        """Bonk your friends or yourself"""
        if member is None:
            member = ctx.author
        url5 = SFW['bonk1']
        r5 = requests.get(url5)
        data5 = r5.json()
        imgdata = data5['url']
        desc = [
            str(B_MESSAGE['b_msg1']).format(ctx.message.author.mention, member.mention),
            str(B_MESSAGE['b_msg2']).format(ctx.message.author.mention, member.mention),
            str(B_MESSAGE['b_msg3']).format(member.mention),
        ]
        embed = discord.Embed(
            color=discord.Color.green(),
            title="--- Bonk!! ---",
            description=random.choice(desc)
        )
        embed.set_image(url=imgdata)
        embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
            
        await ctx.send(embed=embed)
    
    @commands.command()
    async def meme(ctx):
        """Random Meme Image"""
        url6 = MEME['meme1']
        r6 = requests.get(url6)
        data6 = r6.json()
        imgdata = data6['url']
        desc = [
            str(M_MESSAGE['m_msg1']).format(ctx.message.author.mention),
            str(M_MESSAGE['m_msg2']).format(ctx.message.author.mention),
            str(M_MESSAGE['m_msg3']).format(ctx.message.author.mention),
            str(M_MESSAGE['m_msg4']).format(ctx.message.author.mention),
        ]
        embed = discord.Embed(
            color=discord.Color.green(),
            title=data6['title'],
            description=random.choice(desc)
        )
        embed.set_image(url=imgdata)
        embed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Image(bot))