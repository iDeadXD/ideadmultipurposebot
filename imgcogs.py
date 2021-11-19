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
    
    def __init__(self, bot, message):
        self.bot = bot
        sel
    
    

def setup(bot):
    bot.add_cog(Image(bot))
