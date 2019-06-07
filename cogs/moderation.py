# Author: Davis#9654 | Modified: YeetMachine#1337
from discord.ext import commands
import discord


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.kickMessage = "You have been kicked from CS Army"
        self.banMessage = "You have been banned from CS Army"
        self.kickBanEnd = "If you would like to appeal this kick / ban " \
                          "please get in contact with YeetMachine#1337 or akir-#7891"

    @commands.has_permissions(kick_members=True)
    @commands.command(name="kick")
    async def kick_member(self, ctx, member: commands.MemberConverter, reason="unspecified"):
        """Kicks a member"""
        if await self.bot.yes_no(ctx, f"Are you sure you want to kick {member.mention}?"):
            await member.send(f"{self.kickMessage} for the reason {reason}. {self.kickBanEnd}")
            await ctx.guild.kick(member, reason=reason)
            await ctx.send(f"The member {member} has been kicked")
        else:
            await ctx.send("Ok member will not be kicked!")

    @commands.has_permissions(ban_members=True)
    @commands.command(name="ban")
    async def ban_member(self, ctx, member: commands.MemberConverter, reason="unspecified"):
        """Bans a member"""
        if await self.bot.yes_no(ctx, f"Are you sure you want to ban {member.mention}?"):
            await member.send(f"{self.banMessage} for the reason {reason}. {self.kickBanEnd}")
            await ctx.guild.ban(member, reason=reason)
            await ctx.send(f"The member {member} has been ban")
        else:
            await ctx.send("Ok, member will not be banned!")


def setup(bot):
    bot.add_cog(Moderation(bot))
