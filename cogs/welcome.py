from discord.ext import commands
import discord
from core.general_functions import load_config, update_config


class WelcomeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configs = load_config()
        self.welcome_channel = self.bot.get_channel(self.configs["welcome_id"])

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(title="Welcome!", description=f'{member.name} has Joined the Server!', color=583680)
        await self.welcome_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(title="Goodbye", description=f'{member.name} has Left the Server!', color=16713287)
        await self.welcome_channel.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command(name="set_welcome")
    async def set_welcome_channel(self, ctx, channel: commands.TextChannelConverter):
        self.configs["welcome_id"] = channel.id
        update_config(self.configs)
        await ctx.send(f'Welcome channel updated to: {channel.name}')


def setup(bot):
    bot.add_cog(WelcomeCog(bot))
