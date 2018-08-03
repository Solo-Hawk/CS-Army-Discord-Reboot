import discord
from discord.ext import commands
# standard import for any module
import core.mdb as mdb


class Module:
    def __init__(self, bot: commands.Bot):
        pass

        @bot.group(name='mdb',
                   aliases=['bot', 'master'])
        @commands.is_owner()
        async def mdbcom(ctx: commands.Context):
            pass

        @mdbcom.command(name='add_role')
        @commands.is_owner()
        async def _add_role(ctx: commands.Context, role: discord.Role):
            mdb.add_role(str(role.id))
            await ctx.send(f"Role {role} has been added to auth roles")

        @mdbcom.command(name='remove_role')
        @commands.is_owner()
        async def _remove_role(ctx: commands.Context, role: discord.Role):
            mdb.remove_role(str(role.id))
            await ctx.send(f"Role {role} has been removed from auth roles")
