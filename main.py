# Author: Davis#9654 | Modified: YeetMachine#1337
from discord.ext import commands
from core.DiscordCSBot import DiscordCSBot
import traceback
import discord
import json


async def get_prefix(bot, message):
    default_prefix = bot.get_config(config="default_prefix")
    if not message.guild:
        return default_prefix
    try:
        prefix = bot.get_guild_data(message.guild.id, "prefix")
        if prefix is None:
            bot.guild_data_update(message.guild.id, {"prefix": default_prefix})
            return default_prefix
        return prefix
    except KeyError:
        bot.guild_data_update(message.guild.id, {"prefix": default_prefix})
        return default_prefix


bot = DiscordCSBot(command_prefix=get_prefix)
bot.help_command = commands.MinimalHelpCommand()


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


@bot.event
async def on_guild_join(guild):
    """When bot joins new guild adds data to guild_data.json"""
    bot.guild_data_update(guild.id, {"prefix": bot.get_config(config="default_prefix"), "auth_role": []}, append=False)


if __name__ == '__main__':
    for extension in bot.get_config(config="extensions"):
        try:
            bot.load_extension(extension)
            print(f'Successfully Loaded {extension}')
        except Exception as e:
            traceback.print_exc()
            print(f'Failed to load {extension} Error: {str(e)}')


token = open('core/token.txt').read()
bot.run(token)
