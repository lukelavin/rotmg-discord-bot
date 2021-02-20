import discord

from discord.ext import commands
from discord import utils

def has_rl_perms():
    async def predicate(ctx):
        rl_role = utils.get(ctx.guild.roles, name="RL")
        return ctx.author.top_role >= rl_role
    return commands.check(predicate)

def has_leader_perms():
    async def predicate(ctx):
        if ctx.author.id == 266757195054448641:
            return True
        leader_role = ctx.guild.get_role(691619231459967067)
        return ctx.author.top_role >= rl_role
    return commands.check(predicate)
