# Author: Davis#9654 | Modified: YeetMachine#1337
from discord.ext import commands
import discord


class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        # Check if auto role is set up in guild
        if self.bot.get_guild_data(payload.guild_id, key="auto_role_messages"):
            auto_role_messages = self.bot.get_guild_data(payload.guild_id, key="auto_role_messages")
            # Check if this channel has an auto role message
            if str(payload.channel_id) in auto_role_messages and not user.bot:
                # Check if this message is an auto role message
                if str(payload.message_id) in auto_role_messages[str(payload.channel_id)]:
                    # Go through all reactors for that message
                    for reactor in auto_role_messages[str(payload.channel_id)][str(payload.message_id)]:
                        # If the emoji matches a reactor then we remove the role
                        if self.bot.convert_partial_emoji(payload.emoji) == int(reactor[0]):
                            # Remove the role
                            await user.remove_roles(guild.get_role(int(reactor[1])))
                            # Stop looping
                            break

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        user = guild.get_member(payload.user_id)

        # Check if auto role is set up in guild
        if self.bot.get_guild_data(payload.guild_id, key="auto_role_messages"):
            auto_role_messages = self.bot.get_guild_data(payload.guild_id, key="auto_role_messages")
            # Check if this channel has an auto role message
            if str(payload.channel_id) in auto_role_messages and not user.bot:
                # Check if this message is an auto role message
                if str(payload.message_id) in auto_role_messages[str(payload.channel_id)]:
                    # Go through all reactors for that message
                    for reactor in auto_role_messages[str(payload.channel_id)][str(payload.message_id)]:
                        # If the emoji matches a reactor then we remove the role
                        if self.bot.convert_partial_emoji(payload.emoji) == int(reactor[0]):
                            # Remove the role
                            await user.add_roles(guild.get_role(int(reactor[1])))
                            # Stop looping
                            break

    @commands.has_permissions(administrator=True)
    @commands.group(invoke_without_command=True)
    async def autorole(self, ctx):
        await ctx.send_help(self.autorole)

    @commands.has_permissions(administrator=True)
    @autorole.command(name="add")
    async def add_auto_role_message(self, ctx, channel: commands.TextChannelConverter):
        """Use this command to setup an auto role message"""
        messages = [ctx.message, await ctx.send("Send the message for the auto-role")]

        def check(m):
            return m.author == ctx.message.author and m.channel.id == ctx.message.channel.id

        user_msg = await self.bot.wait_for('message', check=check, timeout=240)
        role_msg = await channel.send(user_msg.content)
        messages.append(user_msg)
        messages.append(await ctx.send("Now its time to add emojis/roles. "
                                       "Add the emojis on to the message you sent "
                                       "then send any message to this channel"))
        messages.append(await self.bot.wait_for('message', check=check, timeout=240))

        reactions = user_msg.reactions
        reactors = []
        for reaction in reactions:
            role = await self.get_role(ctx, f"Send a role for {reaction}")
            await role_msg.add_reaction(reaction)
            reactors.append([self.bot.convert_emoji(str(reaction)), role.id])

        self.bot.guild_data_update(ctx.guild.id, data={
            "auto_role_messages": {
                str(channel.id): {
                    str(role_msg.id): reactors
                }
            }
        })

        for message in messages:
            await message.delete()

    @commands.has_permissions(administrator=True)
    @autorole.command(name="list")
    async def list_auto_role_message(self, ctx):
        if not self.bot.get_guild_data(ctx.guild.id, key="auto_role_messages"):
            await ctx.send("No auto-role messages setup")
        else:
            embed = discord.Embed(title="Server Auto-Role Messages", type='rich')

            for channel, messages in self.bot.guild_data[str(ctx.guild.id)]["auto_role_messages"].items():
                for message in messages:
                    message_contents = (await ctx.guild.get_channel(int(channel)).fetch_message(int(message))).content
                    embed.add_field(name=message,
                                    value=f'Message: ```{message_contents}```\n[Link to Message](https://discordapp.com/channels/{ctx.guild.id}/{channel}/{message})',
                                    inline=False)

            await ctx.send(embed=embed)

    @commands.has_permissions(administrator=True)
    @autorole.command(name="delete")
    async def delete_auto_role_message(self, ctx, message_id):
        #  Change to use converter
        guild_data = self.bot.guild_data
        try:
            for channel, messages in self.bot.guild_data[str(ctx.guild.id)]["auto_role_messages"].copy().items():  # loops through channels and messages
                for message in messages.copy():  # for each message
                    if message == message_id:   # if the message matches the one we want to delete
                        del guild_data[str(ctx.guild.id)]["auto_role_messages"][channel][message_id]  # delete the message
                        await ctx.send(f"{message_id} has been deleted successfully")
                        if guild_data[str(ctx.guild.id)]["auto_role_messages"][channel] == {}:  # if no other messages saved for channel then delete channel saved info
                            del guild_data[str(ctx.guild.id)]["auto_role_messages"][channel]
            self.bot.write_guild_data(guild_data)
        except Exception as e:
            await ctx.send("Failed to delete auto_role. Exception: " + str(e))

    async def get_role(self, ctx, prompt):
        """Asks user prompt and then waits till they send a role"""
        def check_message(m):
            return m.author is ctx.message.author and m.channel is ctx.message.channel
        role = ""
        while not isinstance(role, discord.Role):
            msg = await ctx.send(prompt)
            message = await self.bot.wait_for('message', check=check_message, timeout=60)

            if message is "exit":
                break

            try:
                role = await commands.RoleConverter().convert(ctx, message.content)
            except Exception as e:
                ctx.send(e)

            await msg.delete()
            await message.delete()
        if isinstance(role, discord.Role):
            return role
        else:
            return None


def setup(bot):
    bot.add_cog(Roles(bot))
