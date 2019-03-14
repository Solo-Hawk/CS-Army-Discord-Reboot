from discord.ext import commands
import discord
import asyncio
from core.general_functions import load_config
import sys


configs = load_config()

extensions = configs["extensions"]

bot = commands.Bot(command_prefix=configs["prefix"])


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f'Successfully Loaded {extension}')
        except Exception as e:
            print(f'Failed to load {extension} Error: {str(e)}')


token = open('core/token.txt').read()
bot.run(token)
