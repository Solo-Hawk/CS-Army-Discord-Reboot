from discord.ext import commands
from core.general_functions import update_config, load_config, has_auth


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configs = load_config()

    @has_auth()
    @commands.command(name='load', hidden=True)
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully Loaded: {cog}')
            self.configs['extensions'].append(cog)
            update_config(self.configs)

    @has_auth()
    @commands.command(name='unload', hidden=True)
    async def cmd_cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'Error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully Unloaded: {cog}')
            self.configs['extensions'].remove(cog)
            update_config(self.configs)

    @has_auth()
    @commands.command(name='reload', hidden=True)
    async def cog_reload(self, ctx, *, cog: str):
        """Unloads and Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'Error: {type(e).__name__} - {e}')
        else:
            await ctx.send(f'Successfully Reloaded: {cog}')

    @has_auth()
    @commands.command(name='list_cogs', hidden=True)
    async def list_cogs(self, ctx):
        """Command which lists all cogs"""
        cogs = self.bot.cogs

        message = ""
        for cog_class, cog_name in cogs.items():
            message += f'Class: {cog_class} Object: {cog_name}\n'
        await ctx.send(message)

    @has_auth()
    @commands.command(name='reload_all', hidden=True)
    async def reload_all_cogs(self, ctx):
        for extension in self.configs['extensions']:
            try:
                self.bot.unload_extension(extension)
                self.bot.load_extension(extension)
                await ctx.send(f'Successfully Reloaded {extension}')
            except Exception as e:
                await ctx.send(f'Failed to reload {extension} Error: {str(e)}')

    @has_auth()
    @commands.command(name="set_prefix", hidden=True)
    async def set_prefix(self, ctx, prefix):
        self.configs["prefix"] = prefix
        update_config(self.configs)
        await ctx.send(f"Prefix updated to {prefix}")



def setup(bot):
    bot.add_cog(OwnerCog(bot))
