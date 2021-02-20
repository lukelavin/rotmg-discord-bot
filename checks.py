import discord

from discord.ext import commands
from discord import utils

def has_rl_perms():
    async def predicate(ctx):
        rl_role = utils.get(ctx.guild.roles, name="RL")
        return ctx.author.top_role >= rl_role
    return commands.check(predicate)
