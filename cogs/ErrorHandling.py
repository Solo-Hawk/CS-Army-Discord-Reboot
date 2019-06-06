from discord.ext import commands
import traceback
import sys


class CommandErrorHandler(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        ignored_exceptions = (
            commands.CommandNotFound,
            commands.UserInputError
        )

        error = getattr(error, 'original', error)

        if isinstance(error, ignored_exceptions):
            return

        elif isinstance(error, commands.MissingRequiredArgument):
            return await ctx.send_help(ctx.command)

        elif isinstance(error, commands.NotOwner):
            return await ctx.send("This command requires you to be the bot owner")

        elif isinstance(error, commands.DisabledCommand):
            return await ctx.send("That command is currently disabled")

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))


