import logging
import os

from discord.ext import commands

cogs_path = 'cogs'
client = commands.Bot(command_prefix=os.getenv('bot_prefix', default='$'))
logging.basicConfig(level=logging.INFO)

for filename in os.listdir(cogs_path):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

client.run(os.getenv('bot_token'))
