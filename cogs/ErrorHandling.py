from discord.ext import commands
import discord
import traceback
import sys


class CommandErrorHandler(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored_exceptions = (

        )

        error = getattr(error, 'original', error)

        if isinstance(error, ignored_exceptions):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send_help(ctx.command)

        elif isinstance(error, commands.CommandNotFound):
            return await ctx.send("That command does not exist")

        elif isinstance(error, commands.NotOwner):
            return await ctx.send("This command requires you to be the bot owner")

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send("That command is currently disabled")

        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if isinstance(original, discord.Forbidden):
                await ctx.send("The Bot is missing permissions")

            else:
                await ctx.send("Internal Error: " + type(original))

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You are missing permissions for that command")

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)



def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))


