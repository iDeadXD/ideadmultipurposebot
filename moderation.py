import discord
from discord.ext import commands
import asyncio
import pytz
from datetime import datetime
from pymongo import MongoClient
from config import CONFIG

dataclient = MongoClient(CONFIG['mongodb_url'])
database = dataclient['database5']
saved = database['saved_2']

class Moderator(commands.Cog):
    """Moderator related commands. """
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel.id != 851745883825373225: return
        data = saved.find_one({'_id': message.channel.id})
        
        if message.embeds:
            try:
                dev = self.client.get_user(843132313562513408)
                now = datetime.now(pytz.timezone('Asia/Jakarta'))
                
                embed = message.embeds[0]
                embtitle = embed.title
                embdescription = embed.description
                embfooter = embed.footer.text
                embfootericon = embed.footer.icon_url
                embfields = embed.fields
                embimage = embed.image.url
                embthumbnail = embed.thumbnail.url
                embauthoricon = embed.author.icon_url
                embauthorname = embed.author.name
                
                #Identifier
                title = 'None' if len(embtitle) == 0 else embtitle
                description = 'None' if len(embdescription) == 0 else embdescription
                footer = 'None' if len(embfooter) == 0 else embfooter
                footer_icon = 'None' if len(embfootericon) == 0 else embfootericon
                image = 'None' if len(embimage) == 0 else embimage
                fields = 'None' if len(embfields) == 0 else str(len(embfields))
                thumbnail = 'None' if len(embthumbnail) == 0 else embthumbnail
                authoricon = 'None' if len(embauthoricon) == 0 else embauthoricon
                authorname = 'None' if len(embauthorname) == 0 else embauthorname
                
                if data is None:
                    new_data = {'_id': message.channel.id, 'title': f'{title}', 'description': f'{description}', 'fields': f'{fields}', 'footer': f'{footer}', 'footer_icon': f'{footer_icon}', 'image': f'{image}', 'thumbnail': f'{thumbnail}', 'embed_author_name': authorname, 'embed_author_icon': authoricon, 'author': message.author.id}
                    saved.insert_one(new_data)
                    await dev.send(f'New Embed Data has been Saved!\nTimestamp: {now}\nServer: {message.guild.name}\nChannel: {message.channel.mention}\n-----------------------')
                else:
                    saved.update_one({'_id': message.channel.id}, {'$set': {'title': f'{title}', 'description': f'{description}', 'fields': f'{fields}', 'footer': f'{footer}', 'footer_icon': f'{footer_icon}', 'image': f'{image}', 'thumbnail': f'{thumbnail}', 'embed_author_name': authorname, 'embed_author_icon': authoricon, 'author': message.author.id}})
                    await dev.send(f'Embed Data has been Updated!\nTimestamp: {now}\nServer: {message.guild.name}\nChannel: {message.channel.mention}\n-----------------------')
            except Exception as e:
                return print(e)
    
    @commands.command(aliases=['se'])
    async def snipe_embed(self, ctx):
        data = saved.find_one({'_id': ctx.channel.id})
        
        if data is None:
            failed = discord.Embed(
                title='',
                description=f'No Embed was deleted last time on {ctx.channel.mention}',
                color=discord.Color.green()
            )
            return await ctx.send(embed=failed)
        
        author = self.client.get_user(data['author'])
        recreate = discord.Embed(
            title='--- Embed Sniped! ---',
            description=f'Deleted Embed in {ctx.channel.mention}',
            color=discord.Color.purple(),
            timestamp=ctx.message.created_at
        )
        recreate.add_field(name='Title', value=f'{data["title"]}')
        recreate.add_field(name='Description', value=f'{data["description"]}')
        recreate.add_field(name='Footer', value=f'{data["footer"]}')
        recreate.add_field(name='Total Fields', value=f'{data["fields"]}')
        recreate.add_field(name='Footer Icon URL', value=f'{data["footer_icon"]}')
        recreate.add_field(name='Thumbnail URL', value=f'{data["thumbnail"]}')
        recreate.add_field(name='Image URL', value=f'{data["image"]}')
        recreate.add_field(name='Author', value=f'{author.name + "#" + author.discriminator} / {author.mention}')
        recreate.add_field(name='Embed Author Name', value=f'{data["embed_author_name"]}')
        recreate.add_field(name='Embed Author Icon', value=f'{data["embed_author_icon"]}')
        recreate.set_footer(text=f'Sniped by {ctx.author.name + "#" + ctx.author.discriminator}')
        
        await ctx.send(embed=recreate)
    
    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def changename(self, ctx, names=None):
        """Change Nickname for Yourself"""
        if names is None:
            fail1 = discord.Embed(
                title="--- Change Name ---",
                color=discord.Color.red()
            )
            fail1.add_field(name="Change Status", value="Failed!!")
            return await ctx.send(embed=fail1)
        
        changed = discord.Embed(
            title="--- Change Name ---",
            color=discord.Color.purple()
        )
        changed.add_field(name="Change Status", value="Completed!!")
        changed.add_field(name="Name (Before)", value=f"{ctx.message.author.name}")
        changed.add_field(name="Name (After)", value=f"{names}")
        changed.set_footer(text="Requested by {} | Today at {}".format(ctx.message.author.name, datetime.now(pytz.timezone('Asia/Jakarta')).strftime("%H:%M:%S")), icon_url=ctx.message.author.avatar_url)
        
        await ctx.send(embed=changed)
        await asyncio.sleep(2)
        await ctx.message.author.edit(nick=str(names))
    
    @commands.command()
    @commands.has_permissions(manage_guild=True, ban_members=True, kick_members=True)
    async def ban(self, ctx, member : discord.Member=None, *, reason=None):
        try:
            yes = ["y", "yes", "Y"]
            no = ["n", "no", "N"]
            
            if reason is None:
                await ctx.send("Reason required!!")
                return
            if member is ctx.guild.owner and member != None:
                await ctx.send("Owner!!. You can't ban Server Owner")
                return
            if member is None:
                await ctx.send("You have to choose a member to get banned. Command Ignored")
                return
            
            confirm = discord.Embed(
                title="",
                description=f"Are you sure you want to ban {member.mention}? (y/n)",
                color=discord.Color.magenta()
            )
            
            await ctx.send(embed=confirm)
            msg = await self.client.wait_for('message', check=lambda message : message.author == ctx.author and message.channel == ctx.channel, timeout=10)
            if msg.content in yes:
                guild = ctx.guild.name
                await member.ban(reason=reason)
                embed = discord.Embed(
                    title="--- Banned Member ---",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                embed.add_field(name="Member Name", value=f"{member.mention}")
                embed.add_field(name="Punishment", value="Banned from Server")
                embed.add_field(name="Reason", value=f"{reason}")
                embed.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
                
                banned = discord.Embed(
                    title="--- You have been Banned ---",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                banned.add_field(name="Punishment", value="Banned from Server")
                banned.add_field(name="Reason", value=f"{reason}")
                banned.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
                
                await ctx.send(embed=embed)
                await ctx.send("✔ User has been notified.")
                await member.send(embed=banned)
            
            elif msg.content in no:
                cancelled = discord.Embed(
                    title="",
                    description=f"Ban {member.mention} cancelled",
                    color=discord.Color.green()
                )
                
                await ctx.send(embed=cancelled)
        except asyncio.TimeoutError:
            failed = discord.Embed(
                title="",
                description="Ban Timeout",
                color=discord.Color.red()
            )
            return await ctx.send(embed=failed)
    
    @commands.command()
    @commands.has_permissions(manage_guild=True, kick_members=True)
    async def kick(self, ctx, member : discord.Member=None, *, reason=None):
        try:
            yes = ["y", "yes", "Y"]
            no = ["n", "no", "N"]
            
            if reason is None:
                await ctx.send("Reason required!!")
                return
            if member is ctx.guild.owner and member != None:
                await ctx.send("Owner!!. You can't kick Server Owner")
                return
            
            confirm = discord.Embed(
                title="",
                description=f"Are you sure you want to kick {member.mention}? (y/n)",
                color=discord.Color.magenta()
            )
            
            await ctx.send(embed=confirm)
            msg = await self.client.wait_for('message', check=lambda message : message.author == ctx.author and message.channel == ctx.channel, timeout=10)
            if msg.content in yes:
                guild = ctx.guild.name
                await member.kick(reason=reason)
                embed = discord.Embed(
                    title="--- Kicked Member ---",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                embed.add_field(name="Member Name", value=f"{member.mention}")
                embed.add_field(name="Punishment", value="Kicked from Server")
                embed.add_field(name="Reason", value=f"{reason}")
                embed.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
                
                kicked = discord.Embed(
                    title="--- You have been Kicked ---",
                    color=discord.Color.red(),
                    timestamp=ctx.message.created_at
                )
                kicked.add_field(name="Punishment", value="Kicked from Server")
                kicked.add_field(name="Reason", value=f"{reason}")
                kicked.add_field(name="Moderator", value=f"{ctx.message.author.mention}")
                
                await ctx.send(embed=embed)
                await ctx.send("✔ User has been notified.")
                await member.send(embed=kicked)
            
            elif msg.content in no:
                cancelled = discord.Embed(
                    title="",
                    description=f"Kick {member.mention} cancelled",
                    color=discord.Color.green()
                )
                
                await ctx.send(embed=cancelled)
        except asyncio.TimeoutError:
            failed = discord.Embed(
                title="",
                description="Kick Timeout!!"
            )
            return await ctx.send(embed=failed)

def setup(client):
    client.add_cog(Moderator(client))
