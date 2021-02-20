import discord
from datetime import datetime

from discord import DeletedReferencedMessage
from discord.ext import commands

class Core(commands.Cog):
    """Basic commands and miscellaneous things"""

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.is_owner()
    async def delete(self, ctx):
        print(f'[{datetime.now()}] Deleted message with content: "{ctx.message.content}" from #{ctx.channel.name} in <{ctx.guild.name}>')
        await ctx.message.delete()

    @commands.command()
    @commands.is_owner()
    async def ping(self, ctx):
        await ctx.channel.send('pong')

def setup(client):
    print("Added core cog")
    client.add_cog(Core(client))
