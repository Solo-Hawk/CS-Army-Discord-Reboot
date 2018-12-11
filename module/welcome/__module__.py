import discord
from discord.ext import commands
# standard import for any module
import core.mdb as mdb
import json

reactors_config = {}


def get_reactors():
    global reactors_config
    with open('module/welcome/config.json') as json_file:
        reactors_config = json.load(json_file)
    print(reactors_config)
    return reactors_config["reactors"]


def save_reactors():
    global reactors_config
    with open('module/welcome/config.json', 'w') as outfile:
        json.dump(reactors_config, outfile)


def update_reactors(reactors):
    global reactors_config
    reactors_config["reactors"] = reactors
    save_reactors()


def add_reactor(react_message):
    global reactors_config
    print(f"Welcome Reactor - Added {react_message}")
    if react_message in reactors_config["reactors"]:
        return
    reactors_config["reactors"].append(react_message)
    save_reactors()


def remove_reactor(react_message):
    global reactors_config
    print(f"Welcome Reactor - Removed {react_message}")
    reactors_config["reactors"].remove(react_message)
    save_reactors()


class Module:
    def __init__(self, bot: commands.Bot):
        pass

        @bot.listen('on_ready')
        async def _init():
            get_reactors()

        @bot.listen('on_raw_reaction_add')
        async def react_received(emoji, message_id, channel_id, user_id):
            reactors = get_reactors()
            if message_id not in [reactor["message"] for reactor in reactors]:
                return

            channel = bot.get_channel(channel_id)
            guild = channel.guild

            reactor = discord.utils.find(lambda reactor: reactor["message"] == message_id, reactors)
            reaction_set = discord.utils.find(lambda reactor: reactor["reaction"] == emoji.id, reactor["reactors"])
            react_role = discord.utils.find(lambda role: role.id == reaction_set["role"], guild.roles)

            member = guild.get_member(user_id)

            await member.add_roles(react_role)

        @bot.listen('on_raw_reaction_remove')
        async def react_remove(emoji, message_id, channel_id, user_id):
            reactors = get_reactors()
            if message_id not in [reactor["message"] for reactor in reactors]:
                return

            channel = bot.get_channel(channel_id)
            guild = channel.guild

            reactor = discord.utils.find(lambda reactor: reactor["message"] == message_id, reactors)
            reaction_set = discord.utils.find(lambda reactor: reactor["reaction"] == emoji.id, reactor["reactors"])
            react_role = discord.utils.find(lambda role: role.id == reaction_set["role"], guild.roles)

            member = guild.get_member(user_id)

            await member.remove_roles(react_role)

        @bot.group(name='welcome')
        @commands.check(mdb.is_auth_role)
        async def welcome(ctx: commands.Context):
            pass

        @welcome.command(name='create_message')
        async def create_message(ctx: commands.Context, channelID: int):
            channel = bot.get_channel(channelID)
            message = ctx.message

            await message.channel.send("Provide Message")

            def pred(m: discord.Message):
                return m.author == message.author \
                       and m.channel == message.channel

            msg = await bot.wait_for('message', check=pred)

            message = await channel.send(msg.content)

        @welcome.command(name='create_reactor')
        async def create_reactor(ctx: commands.Context, channel_id: int):
            react_message = {}

            channel = bot.get_channel(channel_id)
            message = ctx.message

            def pred(m: discord.Message):
                return m.author == message.author \
                       and m.channel == message.channel

            await message.channel.send("Provide Message")

            msg = await bot.wait_for('message', check=pred)
            message = await channel.send(msg.content)

            react_message["message"] = message.id
            react_message["reactors"] = []

            async def add_reacts():

                def pred_react(r: discord.reaction, u: discord.user):
                    return r.message.id == mes.id

                def pred_role(m: discord.Message):
                    return len(m.role_mentions) == 1

                def pred_new_react(m: discord.Message):
                    return m.content == "y" or m.content == "n"

                reactor = {}

                mes = await ctx.send(">> React to this <<")
                react, user = await bot.wait_for('reaction_add', check=pred_react)
                reactor["reaction"] = react.emoji.id

                # await ctx.send(react)
                # await ctx.send(react.emoji.id)

                await ctx.send("Mention target role")
                mes_role = await bot.wait_for('message', check=pred_role)
                reactor["role"] = mes_role.role_mentions[0].id

                # await ctx.send(mes_role.role_mentions[0])

                react_message["reactors"].append(reactor)
                await message.add_reaction(react.emoji)

                mes = await ctx.send("add another role??")
                mes_repeat = await bot.wait_for('message', check=pred_new_react)

                if mes_repeat.content == "y":
                    await ctx.send("Repeating")
                    await add_reacts()

            await add_reacts()

            add_reactor(react_message)

            await ctx.send("Finished")

        @welcome.command(name='edit_message')
        async def edit_message(ctx: commands.Context, channel_id: int, message_id: int):

            channel = bot.get_channel(channel_id)
            message = await channel.get_message(message_id)
            await ctx.send("``` Original Message ```")
            await ctx.send(message.content)
            await ctx.send("``` Send new message ```")
            new_message_content = await bot.wait_for('message')
            message.edit(content=new_message_content)
            await ctx.send("Edit complete")

        @welcome.command(name='add_reactors')
        async def add_reactors(ctx: commands.Context, channel_id: int, message_id: int):

            async def find_reactor(id, seq):
                for reactor in seq:
                    print(reactor)
                    if reactor["message"] == id:
                        return reactor
                return None

            async def check_emoji(id, seq):
                for reactor in seq:
                    print(reactor)
                    if reactor["reaction"] == id:
                        return False
                return True

            reactors = get_reactors()
            channel = bot.get_channel(channel_id)
            message = await channel.get_message(message_id)
            print(message.content)

            reactor_set = await find_reactor(message_id, reactors)
            if reactor_set is None:
                await ctx.send("Not a reactable (Too be added feature soon)")
                return
            print(reactor_set)

            async def add_reacts():

                def pred_react(r: discord.reaction, u: discord.user):
                    return r.message.id == mes.id and check_emoji(r.emoji.id, reactor_set["reactors"])

                def pred_role(m: discord.Message):
                    return len(m.role_mentions) == 1

                def pred_new_react(m: discord.Message):
                    return m.content == "y" or m.content == "n"

                reactor = {}

                mes = await ctx.send(">> React to this <<")
                react, user = await bot.wait_for('reaction_add', check=pred_react)
                reactor["reaction"] = react.emoji.id

                # await ctx.send(react)
                # await ctx.send(react.emoji.id)

                await ctx.send("Mention target role")
                mes_role = await bot.wait_for('message', check=pred_role)
                reactor["role"] = mes_role.role_mentions[0].id

                # await ctx.send(mes_role.role_mentions[0])

                reactor_set["reactors"].append(reactor)
                await message.add_reaction(react.emoji)

                mes = await ctx.send("add another role??")
                mes_repeat = await bot.wait_for('message', check=pred_new_react)

                if mes_repeat.content == "y":
                    await ctx.send("Repeating")
                    await add_reacts()
            add_reacts()

            pass
            # channel = bot.get_channel(channelID)
            # message = ctx.message
            #
            # await message.channel.send("Provide Message")
            #
            # def pred(m: discord.Message):
            #     return m.author == message.author \
            #            and m.channel == message.channel
            #
            # msg = await bot.wait_for('message', check=pred)
            #
            # message = await channel.send(msg.content)