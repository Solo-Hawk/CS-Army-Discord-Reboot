# Author: Davis#9654 | Modified: YeetMachine#1337
from discord.ext import commands
import discord


class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if self.bot.get_guild_data(member.guild.id, key="welcome_id"):
            embed = discord.Embed(title="Welcome!", description=f'{member.name} has Joined the Server!', color=583680)
            channel = self.bot.get_channel(int(self.bot.get_guild_data(member.guild.id, key="welcome_id")))
            await channel.send(embed=embed)
        await self.update_member_counter(member)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if self.bot.get_guild_data(member.guild.id, key="welcome_id"):
            embed = discord.Embed(title="Goodbye!", description=f'{member.name} has Joined the Server!', color=583680)
            channel = self.bot.get_channel(int(self.bot.get_guild_data(member.guild.id, key="welcome_id")))
            await channel.send(embed=embed)
        await self.update_member_counter(member)

    @commands.has_permissions(administrator=True)
    @commands.command(name="set_welcome")
    async def set_welcome_channel(self, ctx, channel: commands.TextChannelConverter):
        """Given a channel it updates the welcome for that guild"""
        self.bot.guild_data_update(ctx.guild.id, data={"welcome_id": channel.id})

        await ctx.send(f'Welcome channel updated to: {channel.name}')

    @commands.has_permissions(administrator=True)
    @commands.command(name="disable_welcome")
    async def disable_welcome(self, ctx):
        """Disables welcome function for a guild"""
        self.bot.guild_data_update(ctx.guild.id, data={"welcome_id": ""})

        await ctx.send(f'Welcome channel disabled')

    @commands.has_permissions(administrator=True)
    @commands.command(name="set_member_counter")
    async def set_member_counter(self, ctx, channel: commands.VoiceChannelConverter):
        """Given a channel it updates the welcome for that guild"""
        self.bot.guild_data_update(ctx.guild.id, data={"member_counter": channel.id})
        await ctx.send(f'Counter set to: {channel.name}')

    async def update_member_counter(self, ctx):
        if not self.bot.get_guild_data(ctx.guild.id, key="member_counter"):
            return
        channel = self.bot.get_channel(self.bot.get_guild_data(ctx.guild.id, key="member_counter"))
        await channel.edit(name=f"members: {ctx.guild.member_count}")


def setup(bot):
    bot.add_cog(Welcome(bot))
