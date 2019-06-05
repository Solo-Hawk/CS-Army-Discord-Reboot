# Author: YeetMachine#1337
from discord.ext import commands
import discord
from core.BotHelper import BotHelper


class AdministratorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BotHelper = BotHelper(bot)
        self.guild_data = self.BotHelper.get_guild_data()

    @commands.has_permissions(administrator=True)
    @commands.command(name="add_auth_role")
    async def add_auth_role(self, ctx, role: commands.RoleConverter, reason="unspecified"):
        """Adds role to Auth"""
        print(role)
        print(type(role))
        if role.id in self.guild_data[str(ctx.guild.id)]["auth_role"]:
            await ctx.send("Role already added")
            return
        self.guild_data[str(ctx.guild.id)]["auth_role"].append(role.id)
        self.BotHelper.update_guild_data()

    @commands.has_permissions(administrator=True)
    @commands.command(name="remove_auth_role")
    async def remove_auth_role(self, ctx, role: commands.RoleConverter, reason="unspecified"):
        """Adds role to Auth"""
        print(role)
        print(type(role))
        if role.id in self.guild_data[str(ctx.guild.id)]["auth_role"]:
            self.guild_data[str(ctx.guild.id)]["auth_role"].remove(role.id)
            self.BotHelper.update_guild_data()
            await ctx.send("Role removed")
        return

    @commands.has_permissions(administrator=True)
    @commands.command(name="print_message")
    async def print_message(self, ctx, channel: commands.TextChannelConverter):
        messages = [ctx.message, await ctx.send("Send Message")]

        def check(m):
            return m.author == ctx.message.author and m.channel.id == ctx.message.channel.id

        user_msg = await self.bot.wait_for('message', check=check, timeout=240)
        messages.append(user_msg)
        await channel.send(user_msg.content)

    @commands.has_permissions(administrator=True)
    @commands.command(name="edit_message")
    async def edit_message(self, ctx, message: commands.MessageConverter):
        messages = [ctx.message]
        if message.author.id is not self.bot.user.id:
            return
        print("Editing")
        messages.append(await ctx.send("Send Message"))

        def check(m):
            return m.author == ctx.message.author and m.channel.id == ctx.message.channel.id

        user_msg = await self.bot.wait_for('message', check=check, timeout=240)
        await message.edit(content=user_msg.content)

        for message in messages:
            await message.delete()


def setup(bot):
    bot.add_cog(AdministratorCog(bot))
