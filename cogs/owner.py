# Author: Davis#9654
from discord.ext import commands
from discord.ext.commands import errors


def has_auth(f):
    def predicate(ctx):
        print(ctx.message.content)
        auth_ids = ctx.bot.get_config(config="auth_ids")
        return ctx.message.author.id in auth_ids

    return commands.check(predicate)


class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True, hidden=True)
    @commands.is_owner()
    async def owner(self, ctx):
        """Commands for people with access to bot code. Allows for manipulation of cogs"""
        await ctx.send_help(self.owner)

    @owner.command(name='load')
    @commands.is_owner()
    async def _cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully Loaded: {cog}')
            self.bot.config_update({"extensions": [x for x in self.bot.extensions]})

    @owner.command(name='unload')
    @commands.is_owner()
    async def _cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        if cog is 'cogs.owner':
            return await ctx.send("You can not unload this through commands")

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'Error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully Unloaded: {cog}')
            self.bot.config_update({"extensions": [x for x in self.bot.extensions]}, append=False)

    @owner.command(name='reload')
    @commands.is_owner()
    async def _cog_reload(self, ctx, *, cog: str):
        """Unloads and Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully Reloaded: {cog}')

    @owner.command(name='list_cogs')
    @commands.is_owner()
    async def _list_cogs(self, ctx):
        """Command which lists all cogs"""
        cogs = self.bot.cogs

        message = ""
        for cog_name in self.bot.extensions:
            message += f'Name: {cog_name}\n'
        await ctx.send(message)

    @owner.command(name='reload_all')
    @commands.is_owner()
    async def _reload_all_cogs(self, ctx):
        """Reloads all currently loaded extensions"""
        print(self.bot.extensions)
        for extension in self.bot.extensions:
            try:
                self.bot.reload_extension(extension)
                await ctx.send(f'Successfully Reloaded {extension}')
            except Exception as e:
                await ctx.send(f'Failed to reload {extension} Error: {str(e)}')

    @owner.command(name='unload_all')
    @commands.is_owner()
    async def _unload_all_cogs(self, ctx):
        """Unloads all currently loaded extensions"""
        for extension in self.bot.extensions.copy():
            if extension is 'cogs.owner':
                pass
            try:
                self.bot.unload_extension(extension)
                await ctx.send(f'Successfully Unloaded {extension}')
            except Exception as e:
                await ctx.send(f'Failed to reload {extension} Error: {str(e)}')
        self.bot.config_update({"extensions": [x for x in self.bot.extensions]}, append=False)


def setup(bot):
    bot.add_cog(Owner(bot))
