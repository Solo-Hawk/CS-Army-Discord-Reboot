import discord
from discord.ext import commands
# standard import for any module


class Module:
    def __init__(self, bot: commands.Bot):
        async def is_admin(ctx: commands.Context):
            # This will only look for roles that have "admin" in the name.
            # This can be changed for role.id or role.permissions
            return "Admin" in [role.name for role in ctx.author.roles]

        @bot.group(name='admin',
                   help='Set of admin commands',
                   brief='Admin module',
                   description='Admin module for kicking and banning',
                   usage='[sub command]')
        @commands.check(is_admin)
        async def admin(ctx: commands.Context):
            """
            Primary admin command group, used to call sub commands of the admin group
            :param ctx: context passed by command call
            :return:
            """
            return

        @admin.command(name='kick',
                       help='kick selected user and provides them the reason',
                       brief='kicks user',
                       description='Kicking a member will remove the member from the server '
                                   'and will disable all active invites for the user. '
                                   'This user can be invited via new invite links',
                       usage='[member] reason')
        @commands.has_permissions(kick_members=True)
        async def kick(ctx: commands.Context, member: discord.Member, reason: str):
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
        async def ban(ctx: commands.Context, member: discord.Member, reason: str):
            """
            Bans user and provides a reason
            :param ctx: context passed by command call
            :param member: targeted member to ban
            :param reason: reason to ban
            :return:
            """
            await member.send(f"You have been ban by a moderator for the following: `{reason}`")
            await ctx.send(f"Can Ban {member} for {reason}")
