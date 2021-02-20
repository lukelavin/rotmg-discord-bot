import discord
import discord.utils
import logging
import json
import asyncio

import checks

from discord.ext import commands
from datetime import datetime

class Raid(commands.Cog):
    def __init__(self, client, logger):
        self.client = client
        self.logger = logger
        self.raid_channels = ['bot-dev', 'raid']

        with open('data/dungeons.json') as dungeon_file:
            self.dungeon_data = json.load(dungeon_file)

    @commands.command(aliases=["hc"])
    @checks.has_rl_perms()
    async def headcount(self, ctx):
        # get raid channel
        for raid_channel in self.raid_channels:
            channel = discord.utils.get(ctx.guild.text_channels,
                                        name=raid_channel)
            if channel:
                break

        # ensure a channel was found
        if not channel:
            self.logger.error('No adequate channel found for headcount.')
            return
        self.logger.info(f"Got channel {channel}")

        # ask which dungeon
        selector_list = ''.join([f"{self.dungeon_data[i]['portalReact']} {i} - {self.dungeon_data[i]['name']}\n"
                                for i in range(len(self.dungeon_data))])
        select_embed = discord.Embed(
            title='Choose a Headcount',
            description="Respond with the number corresponding to the dungeon you would like to run:\n\n" + selector_list,
            colour=discord.Colour.darker_gray()
        )
        selector_msg = await ctx.channel.send('', embed=select_embed)

        try:
            selection_msg = await self.client.wait_for('message',
                timeout=30,
                check=lambda msg: (msg.author == ctx.author
                    and msg.channel == ctx.channel
                    and msg.content.isdigit())
                )
            selection = int(selection_msg.content)
            if selection < 0 or selection >= len(self.dungeon_data):
                await ctx.channel.send('Invalid selection. Try again by starting a new headcount `$hc`!')
        except asyncio.TimeoutError:
            await selector_msg.delete()
            await ctx.channel.send('Selection took too long. Try again by starting a new headcount `$hc`!')
            return

        # start creating the embed with the dungeon data
        selected_data = self.dungeon_data[selection]
        hc_embed_title = f"Headcount for {selected_data['name']} started by @{ctx.author.display_name}"
        hc_embed_desc_portal = f"React with {selected_data['portalReact']} if you're coming to the raid!"
        hc_embed_desc_keys = f"React with necessary keys ({''.join([key for key in selected_data['keyReacts']])}) if you are willing pop."
        hc_embed_desc_classes = f"React with {''.join([react for react in selected_data['classReacts']])} if you're bringing that class or debuff."

        hc_embed = discord.Embed(
            title=hc_embed_title,
            description=hc_embed_desc_portal + '\n' + hc_embed_desc_keys + '\n' + hc_embed_desc_classes
        )
        hc_embed.set_footer(text='Headcount started ')
        hc_embed.set_thumbnail(url=discord.Embed.Empty)
        hc_embed.set_thumbnail(url=selected_data['thumbnail'])
        hc_embed.timestamp = datetime.utcnow()

        hc_message = await channel.send('@here', embed=hc_embed)

        reacts = [selected_data['portalReact']] + selected_data['keyReacts'] + selected_data['classReacts']
        for react in reacts:
            await hc_message.add_reaction(react)


def setup(client):
    logger = logging.getLogger('raid')
    client.add_cog(Raid(client, logger))
