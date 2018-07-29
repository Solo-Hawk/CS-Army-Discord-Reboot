import discord
from discord.ext import commands
# standard import for any module


class Module:
    def __init__(self, bot: commands.Bot):
        @bot.command(name='greet',
                     help='Says hello')
        async def greet(ctx: commands.Context):
            # default module uses .command() since it shouldn't need a sub group to be called from
            """
            Replies with a friendly "hello"
            :param ctx: context passed by command call
            :return:
            """
            await ctx.send("hello")

        @bot.command(name='ping',
                     help='Shows ping in milliseconds')
        async def ping(ctx: commands.Context):
            # default module uses .command() since it shouldn't need a sub group to be called from
            """
            Replies with ping time in milliseconds
            :param ctx: context passed by command call
            :return:
            """
            await ctx.send(bot.latency)

        @bot.command(name='echo',
                     help='repeats what was passed in the command')
        async def echo(ctx: commands.Context, *, content: str):
            # default module uses .command() since it shouldn't need a sub group to be called from
            """
            Replies with a repeat of command arguments
            :param ctx: context passed by command call
            :param content: user passes arguments
            :return:
            """
            await ctx.send(content)
