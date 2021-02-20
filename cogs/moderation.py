import discord
import logging

from discord.ext import commands

import checks

class Moderation(commands.Cog):
    """Commands to manage messages and users"""
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger

    @commands.command()
    @checks.has_leader_perms()
    async def purge(self, ctx, num_msgs: int):
        await ctx.message.delete()
        await ctx.channel.purge(limit=num_msgs)

def setup(client):
    logger = logging.getLogger('moderation')
    client.add_cog(Moderation(client, logger))
