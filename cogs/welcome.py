from discord.ext import commands
import discord
from core.general_functions import load_config, update_config


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configs = load_config()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="Welcome!", description=f'{member.name} has Joined the Server!', color=583680)
        channel = self.bot.get_channel(int(self.configs["guilds"][str(member.guild.id)]["welcome_id"]))
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="Goodbye", description=f'{member.name} has Left the Server!', color=16713287)
        channel = self.bot.get_channel(int(self.configs["guilds"][str(member.guild.id)]["welcome_id"]))
        await channel.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command(name="set_welcome")
    async def set_welcome_channel(self, ctx, channel: commands.TextChannelConverter):
        """Given a channel it updates the welcome for that guild"""
        self.configs["guilds"][str(channel.guild.id)] = {"welcome_id": str(channel.id)}
        update_config(self.configs)
        await ctx.send(f'Welcome channel updated to: {channel.name}')


def setup(bot):
    bot.add_cog(WelcomeCog(bot))
