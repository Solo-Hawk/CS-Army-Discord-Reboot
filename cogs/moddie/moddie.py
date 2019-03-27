# Author: Davis#9654 built on YeetMachine#1337 original code
from discord.ext import commands
import discord
from core.BotHelper import BotHelper
import json


class ModdieCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BotHelper = BotHelper(bot)
        self.config = self.BotHelper.reload_config()
        self.active_cases = self.get_cases()

    @staticmethod
    def get_cases():
        with open('cogs/moddie/active_cases.json') as json_file:
            active_cases = json.load(json_file)
        return active_cases

    def save_cases(self):
        with open('cogs/moddie/active_cases.json', 'w') as outfile:
            json.dump(self.active_cases, outfile)

    def add_case(self, role: int):
        if role in self.active_cases["cases"]:
            return
        self.active_cases["cases"].append(role)
        self.save_cases()

    def remove_case(self, role: int):
        self.active_cases["cases"].remove(role)
        self.save_cases()

    @commands.command(name="mod")
    async def mod_help(self, ctx):
        if await self.BotHelper.yes_no(ctx, "Would you like to chat with an admin?"):
            reason = await self.BotHelper.get_response(ctx, "Why do you need a moderator?")
            category = self.bot.get_channel(self.config["case_category"])
            guild = self.bot.get_guild(self.config["guild_id"])
            channel = await guild.create_text_channel(name=f"case {ctx.author.id}",
                                                      category=category,
                                                      reason="Moddie Channel")
            await channel.set_permissions(ctx.author, read_messages=True)
            await channel.edit(topic=f"{ctx.author.id}")
            embed = discord.Embed(title=f"{ctx.author.name} Ticket", description=f'Reason: {reason} \n Report By: {ctx.author.mention} \n Calling: <@&{self.config["mod_id"]}>')
            await channel.send(f'{ctx.author.mention} <@&{self.config["mod_id"]}>', embed=embed)
            await ctx.send("A channel has been created with a moderator!")
            self.add_case(ctx.author.id)
        else:
            await ctx.send("Ok! Have fun!")

    @commands.has_permissions(administrator=True)
    @commands.command(name='end',
                      help='Ends discussion thread in moddie',
                      brief='End thread',
                      description='Will close the channel')
    async def _end(self, ctx):
        """
        Deletes the discussion thread between moderators and user
        :param ctx: context passed by command call
        :return:
        """
        if ctx.author.bot:
            return
        if type(ctx.channel) != discord.TextChannel:
            return
        if not ctx.channel.name.startswith("case-"):
            await ctx.send("Not a moddie channel")
            return
        await ctx.send("Removing Channel")
        self.remove_case(int(ctx.channel.topic))
        await ctx.channel.delete(reason="Thread Ended")


def setup(bot):
    bot.add_cog(ModdieCog(bot))
