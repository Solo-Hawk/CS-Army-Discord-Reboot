# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
import discord
from discord.ext import commands
# standard import for any module
import core.mdb as mdb
import json

active_cases = {}


def get_cases():
    global active_cases
    with open('../module/moddie/active_cases.json') as json_file:
        active_cases = json.load(json_file)
    print(active_cases)
    return active_cases["cases"]

def save_cases():
    global active_cases
    with open('../module/moddie/active_cases.json', 'w') as outfile:
        json.dump(active_cases, outfile)

def add_case(role: int):
    global active_cases
    print(f"Moddie - Added {role}")
    if role in active_cases["cases"]:
        return
    active_cases["cases"].append(role)
    save_cases()

def remove_case(role: int):
    global active_cases
    print(f"Moddie - Removed {role}")
    active_cases["cases"].remove(role)
    save_cases()

class Module:

    def __init__(self, bot: commands.Bot):

        def update_config():
            with open('../module/moddie/config.json') as json_file:
                config = json.load(json_file)
            self.guild = bot.get_guild(config["guildid"])
            self.category = bot.get_channel(config["categoryid"])
            self.rolecall = config["rolecall"]


        @bot.listen('on_ready')
        async def _init():
            update_config()
            print(self.guild)
            print(self.category)
            print(self.rolecall)
            get_cases()
            game = discord.Game(name="dm me $$mod to chat")
            await bot.change_presence(status=discord.Status.online, game=game)

        @bot.listen('on_message')
        async def message_received(message: discord.Message):
            if message.author.bot:
                return
            if not type(message.channel) == discord.DMChannel:
                return
            if not message.content.startswith("$$mod"):
                return
            if message.author.id in get_cases():
                await message.channel.send("You already have an active cases with the moderators. "
                                           "Please find the channel under the 'Moddie' category")
                return

            def pred(m: discord.Message):
                return m.author == message.author \
                       and m.channel == message.channel \
                       and (m.content == "y" or m.content == "n")

            await message.channel.send("Would you like to start an admin chat? (y / n)")
            msg = await bot.wait_for('message', check=pred)

            if msg.content == "y":
                user = message.author
                add_case(user.id)
                guild = self.guild
                channel = await guild.create_text_channel(name=f"case {user.id}",
                                                          category=self.category,
                                                          reason="Moddie Channel")
                await channel.set_permissions(message.author, read_messages=True)
                await channel.edit(topic=f"{user.id}")
                await channel.send(f"<@&{self.rolecall}> {user.mention}")
                await message.channel.send("A chat has been created with the moderators in CS Army")
            else:
                await message.channel.send("Okay, will not start an admin chat")

        @bot.group(name='moddie',
                   help='Moddie module',
                   brief='Moddie module',
                   description='Moddie is used to handle communications with Users and Moderators',
                   usage='[sub command]')
        @commands.check(mdb.is_auth_role)
        async def moddie(ctx: commands.Context):
            """

            :param ctx:
            :return:
            """
            return

        @moddie.command(name='end',
                       help='Ends discussion thread in moddie',
                       brief='End thread',
                       description='Will close the channel')
        async def _end(ctx: commands.Context):
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
            remove_case(int(ctx.channel.topic))
            await ctx.channel.delete(reason="Thread Ended")





