from discord.ext import commands
from core.general_functions import load_config, update_config
import discord


class StarboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = load_config()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.message.guild.id) in self.config["guilds"]:  # Checks that guild has starboard configured
            if str(ord(reaction.emoji)) in self.config["starboard_emojis"]:  # if new reaction is a star
                total_stars = 0
                for r in reaction.message.reactions:
                    if str(ord(r.emoji)) in self.config["starboard_emojis"]:  # loops through each reaction and checks if it is a star
                        total_stars += r.count  # if reaction is a star we add the count to total
                if total_stars >= int(self.config["guilds"][str(reaction.message.guild.id)]["starboard_min"]):  # if count is bigger then min we send it to starboard
                    embed = discord.Embed(title="⭐ Starboard ⭐", color=13103696)
                    embed.add_field(value=reaction.message.content)
                    embed.set_author(name=reaction.message.author)
                    await self.bot.get_channel(
                        int(self.config["guilds"][str(reaction.message.guild.id)]["starboard_id"])).send(embed=embed)

    @commands.has_permissions(administrator=True)
    @commands.command(name="setup_starboard")
    async def setup_starboard(self, ctx, channel: commands.TextChannelConverter, min_stars):
        """Setup starboard. Usage: setup_starboard channel min_stars"""
        self.config["guilds"][str(ctx.message.guild.id)]["starboard_id"] = str(channel.id)
        self.config["guilds"][str(ctx.message.guild.id)]["starboard_min"] = min_stars
        update_config(self.config)


def setup(bot):
    bot.add_cog(StarboardCog(bot))
