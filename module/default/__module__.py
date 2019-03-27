import discord
from discord.ext import commands
# This is the primary modules, this operates all admin functions, modifications and role management.
# Removing this modules may cause issues to command access and the ability to modify role and user access


class Module:
    def __init__(self, bot: commands.Bot):
        pass


        # @bot.command(name='greet',
        #         #              help='Says hello')
        #         # async def greet(ctx: commands.Context):
        #         #     # default module uses .command() since it shouldn't need a sub group to be called from
        #         #     """
        #         #     Replies with a friendly "hello"
        #         #     :param ctx: context passed by command call
        #         #     :return:
        #         #     """
        #         #     await ctx.send("hello")
        #
        #         # @bot.command(name='ping',
        #         #              help='Shows ping in milliseconds')
        #         # async def ping(ctx: commands.Context):
        #         #     # default module uses .command() since it shouldn't need a sub group to be called from
        #         #     """
        #         #     Replies with ping time in milliseconds
        #         #     :param ctx: context passed by command call
        #         #     :return:
        #         #     """
        #         #     await ctx.send(f"{'%.2f' % (bot.latency * 1000)} ms")
        #         #
        #         # @bot.command(name='echo',
        #         #              help='repeats what was passed in the command')
        #         # async def echo(ctx: commands.Context, *, content: str):
        #         #     # default module uses .command() since it shouldn't need a sub group to be called from
        #         #     """
        #         #     Replies with a repeat of command arguments
        #         #     :param ctx: context passed by command call
        #         #     :param content: user passes arguments
        #         #     :return:
        #         #     """
        #         #     await ctx.send(content)


