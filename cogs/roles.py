from discord.ext import commands
from core.BotHelper import BotHelper


class RolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BotHelper = BotHelper(bot)
        self.configs = self.BotHelper.get_config()
        self.guild_data = self.BotHelper.get_guild_data()

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if str(reaction.message.id) == self.guild_data[str(reaction.message.guild.id)]["auto_role_message_id"] and not user.bot:
            for reactor in self.guild_data[str(reaction.message.guild.id)]["auto_role_reactors"]:
                if int(self.BotHelper.convert_emoji(str(reaction.emoji))) == int(reactor[0]):
                    await user.remove_roles(reaction.message.guild.get_role(int(reactor[1])))

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(self.BotHelper.convert_emoji(str(reaction.emoji)))
        if str(reaction.message.id) == self.guild_data[str(reaction.message.guild.id)]["auto_role_message_id"] and not user.bot:
            for reactor in self.guild_data[str(reaction.message.guild.id)]["auto_role_reactors"]:
                if self.BotHelper.convert_emoji(str(reaction.emoji)) == int(reactor[0]):
                    await user.add_roles(reaction.message.guild.get_role(int(reactor[1])))

    @commands.has_permissions(administrator=True)
    @commands.command(name="add_auto_role_emoji")
    async def add_emoji(self, ctx, emoji, role: commands.RoleConverter):
        """Takes an emoji and a role and adds it to auto-role message"""
        print(type(emoji))
        print(emoji)
        if "auto_role_channel" in self.guild_data[str(ctx.message.guild.id)]:
            if "auto_role_reactors" not in self.guild_data[str(ctx.message.guild.id)]:
                self.guild_data[str(ctx.message.guild.id)]["auto_role_reactors"] = []

            self.guild_data[str(ctx.message.guild.id)]["auto_role_reactors"].append((self.BotHelper.convert_emoji(emoji), role.id))
            self.BotHelper.update_guild_data()
            await ctx.send("Added emoji successfully")
        else:
            await ctx.send("User add_auto_role_message to add a message first before adding emojis")

    @commands.has_permissions(administrator=True)
    @commands.command(name="add_auto_role_message")
    async def add_message(self, ctx, message: commands.clean_content, channel: commands.TextChannelConverter):
        self.guild_data[str(ctx.message.guild.id)]["auto_role_channel"] = str(channel.id)
        self.guild_data[str(ctx.message.guild.id)]["auto_role_message"] = str(message)
        self.BotHelper.update_guild_data()

        await ctx.send("Added Message")

    @commands.has_permissions(administrator=True)
    @commands.command(name="start_auto_role")
    async def start_auto_rule(self, ctx):
        channel = self.bot.get_channel(int(self.guild_data[str(ctx.message.guild.id)]["auto_role_channel"]))
        message = await channel.send(self.guild_data[str(ctx.message.guild.id)]["auto_role_message"])
        self.guild_data[str(ctx.message.guild.id)]["auto_role_message_id"] = str(message.id)
        self.BotHelper.update_guild_data()
        for r in self.guild_data[str(ctx.message.guild.id)]["auto_role_reactors"]:
            await message.add_reaction(self.BotHelper.convert_emoji(int(r[0])))

    @commands.has_permissions(administrator=True)
    @commands.command(name="auto_role_clear_reactors")
    async def clear_auto_role_reactors(self, ctx):
        self.guild_data[str(ctx.message.guild.id)]["auto_role_reactors"] = []
        self.BotHelper.update_guild_data()
        await ctx.send("Done!")


def setup(bot):
    bot.add_cog(RolesCog(bot))
