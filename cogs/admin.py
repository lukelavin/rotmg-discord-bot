import discord
import logging

from discord.ext import commands
from index import cogs_path

class Admin(commands.Cog):
    """Admin commands to dynamically manage modules."""
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

    @commands.command(hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, module: str):
        self.client.unload_extension(cogs_path + '.' + module)
        self.client.load_extension(cogs_path + '.' + module)

        self.logger.info(f'{module} module unloaded.')
        await ctx.channel.send(f'{module} module reloaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, module: str):
        self.client.load_extension(cogs_path + '.' + module)

        self.logger.info(f'{module} module unloaded.')
        await ctx.channel.send(f'{module} module loaded.')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, module: str):
        self.client.unload_extension(cogs_path + '.' + module)

        self.logger.info(f'{module} module unloaded.')
        await ctx.channel.send(f'{module} module unloaded.')

def setup(client):
    logger = logging.getLogger('admin')
    client.add_cog(Admin(client, logger))
