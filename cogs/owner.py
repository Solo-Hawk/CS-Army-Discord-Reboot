from discord.ext import commands
import json


class OwnerCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open("core/configs.json") as r:
            self.configs = json.load(r)

    @commands.command(name='load', hidden=True)
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        if self.check_auth(ctx.author.id) and cog is not 'cogs.owner':
            try:
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f'Error: {type(e).__name__} - {e}')
            else:
                await ctx.send(f'Successfully Loaded: {cog}')
                self.configs['extensions'].add(cog)

                with open('core/configs.json', 'w') as r:
                    json.dump(self.configs, r)

    @commands.command(name='unload', hidden=True)
    async def cmd_cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""
        if self.check_auth(ctx.author.id) and cog is not 'cogs.owner':
            try:
                self.bot.unload_extension(cog)
            except Exception as e:
                await ctx.send(f'Error: {type(e).__name__} - {e}')
            else:
                await ctx.send(f'Successfully Unloaded: {cog}')
                self.configs['extensions'].remove(cog)

                with open('core/configs.json', 'w') as r:
                    json.dump(self.configs, r)

    @commands.command(name='reload', hidden=True)
    async def cog_reload(self, ctx, *, cog: str):
        if self.check_auth(ctx.author.id):
            try:
                self.bot.unload_extension(cog)
                self.bot.load_extension(cog)
            except Exception as e:
                await ctx.send(f'Error: {type(e).__name__} - {e}')
            else:
                await ctx.send(f'Successfully Reloaded: {cog}')

    @commands.command(name='list_cogs', hidden=True)
    async def list_cogs(self, ctx):
        """Command which lists the cogs"""
        if self.check_auth(ctx.author.id):
            cogs = self.bot.cogs
            for cog_class, cog_name in cogs.items():
                await ctx.send(f'Class: {cog_class} Object: {cog_name}')

    def check_auth(self, check_id):
        """Returns True if given ID is in configs as an authenticated moderator"""
        if check_id in self.configs["auth_ids"]:
            return True
        return False


def setup(bot):
    bot.add_cog(OwnerCog(bot))