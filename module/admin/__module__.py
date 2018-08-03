# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
import discord
from discord.ext import commands
# standard import for any module
import core.mdb as mdb


class Module:
    def __init__(self, bot: commands.Bot):

        @bot.group(name='admin',
                   help='Set of admin commands',
                   brief='Admin module',
                   description='Admin module for kicking and banning',
                   usage='[sub command]')
        @commands.check(mdb.is_auth_role)
        async def admin(ctx: commands.Context):
            """
            Primary admin command group, used to call sub commands of the admin group
            :param ctx: context passed by command call
            :return:
            """
            return

        @admin.command(name='usable',
                       help='Confirms rights to use admin commands',
                       brief='Confirms rights',
                       description='Will return a message stating that you can use admin commands'
                                   'blank response or errors will mean you cannot')
        async def _usable(ctx: commands.Context):
            """
            Kicks user and provides a reason
            :param ctx: context passed by command call
            :param member: targeted member to kick
            :param reason: reason to kick
            :return:
            """
            await ctx.send("Confirmed")

        @admin.command(name='kick',
                       help='kick selected user and provides them the reason',
                       brief='kicks user',
                       description='Kicking a member will remove the member from the server '
                                   'and will disable all active invites for the user. '
                                   'This user can be invited via new invite links',
                       usage='[member] reason')
        @commands.has_permissions(kick_members=True)
        async def _kick(ctx: commands.Context, member: discord.Member, reason: str):
            """
            Kicks user and provides a reason
            :param ctx: context passed by command call
            :param member: targeted member to kick
            :param reason: reason to kick
            :return:
            """
            await member.send(f"You have been kick by a moderator for the following: `{reason}`")
            await ctx.message.guild.kick(member, reason=reason)

        @admin.command(name='ban',
                       help='ban selected user',
                       brief='ban user',
                       description='Banning a member will not allow them to join via any active and new invite links '
                                   'until unbanned',
                       usage='[member] reason')
        @commands.has_permissions(ban_members=True)
        async def _ban(ctx: commands.Context, member: discord.Member, reason: str):
            """
            Bans user and provides a reason
            :param ctx: context passed by command call
            :param member: targeted member to ban
            :param reason: reason to ban
            :return:
            """
            await member.send(f"You have been ban by a moderator for the following: `{reason}`")
            await ctx.send(f"Can Ban {member} for {reason}")
