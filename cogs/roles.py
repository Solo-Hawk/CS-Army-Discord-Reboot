from discord.ext import commands
from core.general_functions import load_config, update_config


class RolesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.configs = load_config()

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if str(reaction.message.id) == self.configs["guilds"][str(reaction.message.guild.id)]["auto_role_message_id"]:
            for reactor in self.configs["guilds"][str(reaction.message.guild.id)]["auto_role_reactors"]:
                if reaction.emoji.id == int(reactor[0]) and user.id is not self.bot.id:
                    await user.add_roles(reaction.message.guild.get_role(int(reactor[1])))

    @commands.has_permissions(administrator=True)
    @commands.command(name="add_auto_role_emoji")
    async def add_emoji(self, ctx, emoji: commands.EmojiConverter, role: commands.RoleConverter):
        """Takes an emoji and a role and adds it to auto-role message"""
        if "auto_role_channel" in self.configs["guilds"][str(ctx.message.guild.id)]:
            if "auto_role_reactors" not in self.configs["guilds"][str(ctx.message.guild.id)]:
                self.configs["guilds"][str(ctx.message.guild.id)]["auto_role_reactors"] = []

            self.configs["guilds"][str(ctx.message.guild.id)]["auto_role_reactors"].append((emoji.id, role.id))
            update_config(self.configs)
            await ctx.send("Added emoji successfully")
        else:
            await ctx.send("User add_auto_role_message to add a message first before adding emojis")

    @commands.has_permissions(administrator=True)
    @commands.command(name="add_auto_role_message")
    async def add_message(self, ctx, message: commands.clean_content, channel: commands.TextChannelConverter):
        if not str(ctx.message.guild.id) in self.configs["guilds"]:
            self.configs["guilds"][str(ctx.message.guild.id)] = {}
        self.configs["guilds"][str(ctx.message.guild.id)]["auto_role_channel"] = str(channel.id)
        self.configs["guilds"][str(ctx.message.guild.id)]["auto_role_message"] = str(message)
        update_config(self.configs)

        await ctx.send("Added Message")

    @commands.has_permissions(administrator=True)
    @commands.command(name="start_auto_role")
    async def start_auto_rule(self, ctx):
        channel = self.bot.get_channel(int(self.configs["guilds"][str(ctx.message.guild.id)]["auto_role_channel"]))
        message = await channel.send(self.configs["guilds"][str(ctx.message.guild.id)]["auto_role_message"])
        self.configs["guilds"][str(ctx.message.guild.id)]["auto_role_message_id"] = str(message.id)
        update_config(self.configs)
        for r in self.configs["guilds"][str(ctx.message.guild.id)]["auto_role_reactors"]:
            await message.add_reaction(self.bot.get_emoji(int(r[0])))

    @commands.has_permissions(administrator=True)
    @commands.command(name="auto_role_clear_reactors")
    async def clear_auto_role_reactors(self, ctx):
        self.configs["guilds"][str(ctx.message.guild.id)]["auto_role_reactors"] = []
        update_config(self.configs)
        await ctx.send("Done!")


def setup(bot):
    bot.add_cog(RolesCog(bot))
