# Author: Davis#9654 || Modified: YeetMachine#1337
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
    async def on_raw_reaction_add(self, payload):
        # TODO: Clean this up
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        emoji = self.BotHelper.convert_partial_emoji(payload.emoji)
        total_stars = 0
        if payload.message_id in self.guild_data[str(payload.guild_id)]["starboard_messages"]:
            return
        if emoji in self.configs["starboard_emotes"] and "starboard_min" in self.guild_data[str(payload.guild_id)]:
            message = await channel.fetch_message(payload.message_id)
            for r in message.reactions:
                # loops through each reaction and checks if it is a star
                if self.BotHelper.convert_emoji(r.emoji) in self.configs["starboard_emotes"]:
                    total_stars += r.count  # if reaction is a star we add the count to total
            # if count is bigger then min we send it to starboard
            # from "total_stars >=" to "total_stars ==" since reacts after the minimum will re-post message to starboard
            if total_stars == int(self.guild_data[str(payload.guild_id)]["starboard_min"]):
                embed = discord.Embed(color=13103696,
                                      description=f'{message.content}\n [Jump To](https://discordapp.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id})')
                embed.set_footer(text=f"Author: {message.author}", icon_url=message.author.avatar_url)
                await self.bot.get_channel(
                    int(self.guild_data[str(payload.guild_id)]["starboard_id"])).send(embed=embed)
                # once added, message is added so it cannot be re-starred
                self.guild_data[str(payload.guild_id)]["starboard_messages"].append(payload.message_id)
                self.BotHelper.update_guild_data()

    @commands.has_permissions(administrator=True)
    @commands.command(name="setup_starboard")
    async def setup_starboard(self, ctx, channel: commands.TextChannelConverter, min_stars):
        """Setup starboard. Usage: setup_starboard #channel min_stars"""
        self.guild_data[str(ctx.guild.id)]["starboard_id"] = str(channel.id)
        self.guild_data[str(ctx.guild.id)]["starboard_min"] = min_stars
        # Array is used for storing message ids of starred messages
        self.guild_data[str(ctx.guild.id)]["starboard_messages"] = []
        self.BotHelper.update_guild_data()

        await ctx.send("Starboard Setup")

    @setup_starboard.error
    async def setup_starboard_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f'Usage: {self.BotHelper.get_guild_data()[str(ctx.guild.id)]["prefix"]}setup_starboard #channel min_stars')


def setup(bot):
    bot.add_cog(StarboardCog(bot))
