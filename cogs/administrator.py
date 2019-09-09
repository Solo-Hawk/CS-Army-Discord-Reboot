# Author: YeetMachine#1337 | Modified: Davis#9654
from discord.ext import commands
import discord


class Administrator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.has_permissions(administrator=True)
    @commands.command(name="add_auth_role")
    async def add_auth_role(self, ctx, role: commands.RoleConverter):
        """Adds role to Auth"""
        print(role)
        print(type(role))
        if role.id in self.bot.get_guild_data(ctx.guild.id, key="auth_role"):
            await ctx.send("Role already added")
            return
        self.bot.guild_data_update(ctx.guild.id, {"auth_role": role.id}, append=True)

    @commands.has_permissions(administrator=True)
    @commands.command(name="remove_auth_role")
    async def remove_auth_role(self, ctx, role: commands.RoleConverter):
        """Adds role to Auth"""
        print(role)
        print(type(role))
        if role.id in self.bot.get_guild_data(ctx.guild.id, key="auth_role"):
            auth_roles = self.bot.get_guild_data(ctx.guild.id, key="auth_role")
            self.bot.guild_data_update(ctx.guild.id, data={"auth_roles": auth_roles.remove(role.id)}, append=False)
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
    bot.add_cog(Administrator(bot))