# Author: Davis#9654
from discord.ext import commands
import discord
from core.BotHelper import BotHelper


def get_prefix(bot, message):
    """Returns prefix for bot, currently this allows for changing prefix in future could implement per-server
    prefix"""
    return BotHelper.get_guild_data()[str(message.guild.id)]["prefix"]


bot = commands.Bot(command_prefix=get_prefix)
BotHelper = BotHelper(bot)


@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}\n')


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CommandNotFound):
        await ctx.send("That command is not recognized")
    else:
        raise error


@bot.event
async def on_guild_join(guild):
    """When bot joins ne guild adds data to guild_data.json"""
    guild_data = BotHelper.get_guild_data()
    guild_data[str(guild.id)] = {"prefix": "$$"}
    BotHelper.update_guild_data()


if __name__ == '__main__':
    for extension in BotHelper.get_config()["extensions"]:
        try:
            bot.load_extension(extension)
            print(f'Successfully Loaded {extension}')
        except Exception as e:
            print(f'Failed to load {extension} Error: {str(e)}')

token = open('core/token.txt').read()
bot.run(token)
