import discord
import asyncio
from discord.ext import commands
# standard import for any module
import core.mdb as mdb



class Module:
    def __init__(self, bot: commands.Bot):
        pass

        @bot.group(name='dev',
                   aliases=['developer'])
        @commands.check(mdb.is_auth_role)
        async def developer(ctx: commands.Context):
            pass

        @developer.command(name='debug')
        async def _debug(ctx: commands.Context, *args):
            await ctx.send(f"```{args}```")
            await ctx.send(f"```{ctx.message}```")
            await ctx.send(f"{ctx.message.content[len(ctx.invoked_with) + len(ctx.command.name) + 2:]}")\

        @developer.command(name='get_roles')
        async def _get_roles(ctx: commands.Context, *args):
            roles = ctx.channel.guild.roles
            msg = "```\n"
            for role in roles:
                msg += role.name + " : " + str(role.id) + "\n"
            msg += "```"
            await ctx.send(msg)
        @developer.command(name='say')
        async def _say(ctx: commands.Context, channelID: int, *args):
            channel = bot.get_channel(channelID)
            shift = len(ctx.invoked_with) + len(ctx.command.name) + len(str(channelID)) + 5
            await channel.send(f"{ctx.message.content[shift:]}")

        @developer.command(name='say_emoji')
        async def _say_emoji(ctx: commands.Context):
            message = await ctx.send(">> React to this <<")

            def check(r: discord.reaction, u: discord.user):
                print(r)
                print(r.emoji.id)
                print(message)
                print(r.message.id == message.id)
                return r.message.id == message.id

            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('👎')
            else:
                await ctx.send(f'{reaction.emoji.id}')
                await ctx.send(f'{reaction.emoji.name}')
                await ctx.send(reaction)







