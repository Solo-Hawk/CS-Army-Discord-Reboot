from discord.ext import commands
from core.BotHelper import BotHelper
import discord


class StarboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BotHelper = BotHelper(bot)
        self.configs = self.BotHelper.get_config()
        self.guild_data = self.BotHelper.get_guild_data()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):  # THIS NEEDS CLEANED UP
            total_stars = 0
            if reaction.emoji in ["⭐", "🌟"] and "starboard_min" in self.guild_data[str(reaction.message.guild.id)].keys():
                for r in reaction.message.reactions:
                    if str(r.emoji) in ["⭐", "🌟"]:  # loops through each reaction and checks if it is a star
                        total_stars += r.count  # if reaction is a star we add the count to total
                if total_stars >= int(self.guild_data[str(reaction.message.guild.id)]["starboard_min"]):  # if count is bigger then min we send it to starboard
                    embed = discord.Embed(title="⭐ Starboard ⭐", color=13103696, description=reaction.message.content)
                    embed.set_footer(text=f"Author: {reaction.message.author}", icon_url=reaction.message.author.avatar_url)
                    await self.bot.get_channel(
                        int(self.guild_data[str(reaction.message.guild.id)]["starboard_id"])).send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command(name="setup_starboard")
    async def setup_starboard(self, ctx, channel: commands.TextChannelConverter, min_stars):
        """Setup starboard. Usage: setup_starboard #channel min_stars"""
        self.guild_data[str(ctx.message.guild.id)]["starboard_id"] = str(channel.id)
        self.guild_data[str(ctx.message.guild.id)]["starboard_min"] = min_stars
        self.BotHelper.update_guild_data()

        await ctx.send("Starboard Setup")


def setup(bot):
    bot.add_cog(StarboardCog(bot))
