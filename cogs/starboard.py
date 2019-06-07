# Author: Davis#9654 || Modified: YeetMachine#1337
from discord.ext import commands
import discord


class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        # TODO: Clean this up
        guild = self.bot.get_guild(payload.guild_id)
        channel = guild.get_channel(payload.channel_id)
        emoji = str(payload.emoji)
        total_stars = 0
        if payload.message_id in self.bot.get_guild_data(guild.id, key="starboard_messages"):
            return
        if emoji in ["⭐", "	🌟"] and self.bot.get_guild_data(guild.id, "starboard_min") is not None:
            message = await channel.fetch_message(payload.message_id)
            for r in message.reactions:
                # loops through each reaction and checks if it is a star
                if r.emoji in ["⭐", "🌟"]:
                    total_stars += r.count  # if reaction is a star we add the count to total
            # if count is bigger then min we send it to starboard
            # from "total_stars >=" to "total_stars ==" since reacts after the minimum will re-post message to starboard
            if total_stars == int(self.bot.get_guild_data(guild.id, "starboard_min")):
                embed = discord.Embed(color=13103696,
                                      description=f'{message.content}\n [Jump To](https://discordapp.com/channels/{payload.guild_id}/{payload.channel_id}/{payload.message_id})')
                embed.set_footer(text=f"Author: {message.author}", icon_url=message.author.avatar_url)
                await self.bot.get_channel(
                    int(self.bot.get_guild_data(guild.id, "starboard_id"))).send(embed=embed)
                # once added, message is added so it cannot be re-starred
                self.bot.guild_data_update(guild.id, {"starboard_messages": [payload.message_id]})

    @commands.group(invoke_without_command=True)
    async def starboard(self, ctx):
        if self.bot.get_guild_data(ctx.guild.id, "starboard_min") is not None:
            await ctx.send_help(self.starboard)
        else:
            await ctx.send("Starboard is not setup in this guild")

    @commands.has_permissions(administrator=True)
    @starboard.command(name="setup")
    async def setup(self, ctx, channel: commands.TextChannelConverter, min_stars):
        """Setup starboard for a guild."""
        self.bot.guild_data_update(ctx.guild.id, {"starboard_id": str(channel.id)})
        self.bot.guild_data_update(ctx.guild.id, {"starboard_min": min_stars})
        # Array is used for storing message ids of starred messages
        self.bot.guild_data_update(ctx.guild.id, {"starboard_messages": []}, append=False)

        await ctx.send("Starboard Setup")

    @starboard.command(name="min")
    async def _min(self, ctx):
        min_stars = self.bot.get_guild_data(ctx.guild.id, key="starboard_min")
        if min_stars is not None:
            await ctx.send(f'Minimum Stars to get added to Starboard: {min_stars}')
        else:
            await ctx.send("Starboard not setup in this guild.")

    @starboard.command(name="channel")
    async def _channel(self, ctx):
        channel_id = self.bot.get_guild_data(ctx.guild.id, key="starboard_id")
        if channel_id is not None:
            await ctx.send(f"Starboard Channel: <#{channel_id}>")
        else:
            await ctx.send("Starboard not setup in this guild.")


def setup(bot):
    bot.add_cog(Starboard(bot))
