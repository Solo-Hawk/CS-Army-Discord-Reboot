# Author: Davis#9654 | Modified: YeetMachine#1337
from discord.ext import commands
import discord
from core.BotHelper import BotHelper


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BotHelper = BotHelper(bot)
        self.kickMessage = "You have been kicked from CS Army"
        self.banMessage = "You have been banned from CS Army"
        self.kickBanEnd = "If you would like to appeal this kick / ban " \
                          "please get in contact with YeetMachine#1337 or akir-#7891"

    @commands.has_permissions(kick_members=True)
    @commands.command(name="kick")
    async def kick_member(self, ctx, member: commands.MemberConverter, reason="unspecified"):
        """Kicks a member"""
        if await self.BotHelper.yes_no(ctx, f"Are you sure you want to kick {member.mention}?"):
            await member.send(f"{self.kickMessage} for the reason {reason}. {self.kickBanEnd}")
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f"The member {member} has been kicked")
        else:
            await ctx.send("Ok member will not be kicked!")

    @kick_member.error
    async def kick_member_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that member...')

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permissions to kick that member")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Usage: {self.BotHelper.get_prefix(self.bot, ctx.message)}kick #member')

        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if isinstance(original, discord.errors.Forbidden):
                await ctx.send("The Bot is missing permissions")

            else:
                await ctx.send("Internal Error: " + type(original))

        else:
            await ctx.send("Error: " + type(error))

    @commands.has_permissions(ban_members=True)
    @commands.command(name="ban")
    async def ban_member(self, ctx, member: commands.MemberConverter, reason="unspecified"):
        """Bans a member"""
        if await self.BotHelper.yes_no(ctx, f"Are you sure you want to ban {member.mention}?"):
            await member.send(f"{self.banMessage} for the reason {reason}. {self.kickBanEnd}")
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"The member {member} has been ban")
        else:
            await ctx.send("Ok, member will not be banned!")

    @ban_member.error
    async def ban_member_error(self, ctx, error):
        if isinstance(error, commands.BadArgument):
            await ctx.send('I could not find that member...')

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permissions to ban that member")

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Usage: {self.BotHelper.get_prefix(self.bot, ctx.message)}ban #member')

        elif isinstance(error, commands.CommandInvokeError):
            original = error.original
            if isinstance(original, discord.errors.Forbidden):
                await ctx.send("The Bot is missing permissions")

            else:
                await ctx.send("Internal Error: " + type(original))

        else:
            await ctx.send("Error: " + type(error))


def setup(bot):
    bot.add_cog(ModerationCog(bot))