from discord.ext import commands
import discord
import asyncio
import json
import sys

with open('core/configs.json') as r:
    configs = json.load(r)

extensions = configs["extensions"]

bot = commands.Bot(command_prefix=configs["prefix"])


@bot.event
async def on_ready():
    print(
        f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


@bot.command(name="kill", hidden=True, pass_context=True)
async def kill(ctx):
    if ctx.author.id in configs["auth_ids"]:
        sys.exit()

if __name__ == '__main__':
    for extension in extensions:
        try:
            bot.load_extension(extension)
            print(f'Successfully Loaded {extension}')
        except Exception as e:
            print(f'Failed to load {extension} Error: {str(e)}')


token = open('core/token.txt').read()
bot.run(token)
