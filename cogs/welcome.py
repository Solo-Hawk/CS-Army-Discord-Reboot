# Author: Davis#9654
from discord.ext import commands
import discord
from core.BotHelper import BotHelper


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BotHelper = BotHelper(bot)
        self.configs = self.BotHelper.get_config()
        self.guild_data = self.BotHelper.get_guild_data()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if "welcome_id" in self.guild_data[str(member.guild.id)]:
            embed = discord.Embed(title="Welcome!", description=f'{member.name} has Joined the Server!', color=583680)
            channel = self.bot.get_channel(int(self.guild_data[str(member.guild.id)]["welcome_id"]))
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if "welcome_id" in self.guild_data[str(member.guild.id)]:
            embed = discord.Embed(title="Goodbye", description=f'{member.name} has Left the Server!', color=16713287)
            channel = self.bot.get_channel(int(self.guild_data[str(member.guild.id)]["welcome_id"]))
            await channel.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command(name="set_welcome")
    async def set_welcome_channel(self, ctx, channel: commands.TextChannelConverter):
        """Given a channel it updates the welcome for that guild"""
        self.guild_data[str(ctx.guild.id)]["welcome_id"] = str(channel.id)
        self.BotHelper.update_guild_data()
        await ctx.send(f'Welcome channel updated to: {channel.name}')

    @set_welcome_channel.error
    async def set_welcome_channel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            ctx.send(f"Usage: {self.guild_data[str(ctx.guild.id)]['prefix']}set_welcome #channel")
        else:
            raise error

    @commands.has_permissions(administrator=True)
    @commands.command(name="disable_welcome")
    async def disable_welcome(self, ctx):
        """Disables welcome function for a guild"""
        self.guild_data[str(ctx.guild.id)]["welcome_id"] = ""
        self.BotHelper.update_guild_data()
        await ctx.send(f'Welcome channel disabled')


def setup(bot):
    bot.add_cog(WelcomeCog(bot))
