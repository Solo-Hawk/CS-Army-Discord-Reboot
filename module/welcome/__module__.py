import discord
from discord.ext import commands
# standard import for any module
import core.mdb as mdb
import json

react_messages = {}


def get_reactors():
    global react_messages
    with open('../module/welcome/config.json') as json_file:
        react_messages = json.load(json_file)
    print(react_messages)
    return react_messages["reactors"]


def save_reactors():
    global react_messages
    with open('../module/welcome/config.json', 'w') as outfile:
        json.dump(react_messages, outfile)


def add_reactor(react_message):
    global react_messages
    print(f"Welcome Reactor - Added {react_message}")
    if react_message in react_messages["reactors"]:
        return
    react_messages["reactors"].append(react_message)
    save_reactors()


def remove_reactor(react_message):
    global react_messages
    print(f"Welcome Reactor - Removed {react_message}")
    react_messages["reactors"].remove(react_message)
    save_reactors()


class Module:
    def __init__(self, bot: commands.Bot):
        pass

        @bot.listen('on_ready')
        async def _init():
            get_reactors()

        @bot.listen('on_raw_reaction_add')
        async def react_recieved(emoji, message_id, channel_id, user_id):
            channel = bot.get_channel(channel_id)
            reactors = get_reactors()
            if message_id not in [reactor["message"] for reactor in reactors]:
                return
            reactor = discord.utils.find(lambda reactor: reactor["message"] == message_id, reactors)
            message = await channel.get_message(reactor["message"])
            guild = channel.guild
            print(guild)
            # reaction = discord.utils.find(lambda react: react.emoji.id == emoji.id, message.reactions)
            reaction_set = discord.utils.find(lambda reactor: reactor["reaction"] == emoji.id, reactor["reactors"])
            role = discord.utils.find(lambda role: role.id == reaction_set["role"], guild.roles)
            member = guild.get_member(user_id)
            print(member)
            print(role)
            await member.add_roles(role)

        @bot.listen('on_raw_reaction_remove')
        async def react_remove(emoji, message_id, channel_id, user_id):
            channel = bot.get_channel(channel_id)
            reactors = get_reactors()
            if message_id not in [reactor["message"] for reactor in reactors]:
                return
            reactor = discord.utils.find(lambda reactor: reactor["message"] == message_id, reactors)
            message = await channel.get_message(reactor["message"])
            guild = channel.guild
            print(guild)
            # reaction = discord.utils.find(lambda react: react.emoji.id == emoji.id, message.reactions)
            reaction_set = discord.utils.find(lambda reactor: reactor["reaction"] == emoji.id, reactor["reactors"])
            role = discord.utils.find(lambda role: role.id == reaction_set["role"], guild.roles)
            member = guild.get_member(user_id)
            print(member)
            print(role)
            await member.remove_roles(role)





        @bot.group(name='welcome')
        @commands.is_owner()
        async def welcome(ctx: commands.Context):
            pass

        @welcome.command(name='createReact')
        @commands.is_owner()
        async def createReact(ctx: commands.Context, channelID: int, *args):
            react_message = {}
            channel = bot.get_channel(channelID)
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
                    print(r)
                    print(r.emoji.id)
                    return r.message.id == mes.id

                def pred_role(m: discord.Message):
                    print(m)
                    print(m.role_mentions)
                    print(len(m.role_mentions))
                    return len(m.role_mentions) == 1

                def pred_newreact(m: discord.Message):
                    print(m)
                    return m.content == "y" or m.content == "n"
                reactor = {}
                mes = await ctx.send(">> React to this <<")

                react, user = await bot.wait_for('reaction_add', check=pred_react)
                await ctx.send(react)
                await ctx.send(react.emoji.id)
                reactor["reaction"] = react.emoji.id
                mes = await ctx.send("Mention target role")

                mes_role = await bot.wait_for('message', check=pred_role)
                await ctx.send(mes_role.role_mentions[0])
                reactor["role"] = mes_role.role_mentions[0].id

                react_message["reactors"].append(reactor)
                await message.add_reaction(react.emoji)

                mes = await ctx.send("add another role??")

                mes_repeat = await bot.wait_for('message', check=pred_newreact)

                if mes_repeat.content == "y":
                    await ctx.send("Repeating")
                    await add_reacts()


            await add_reacts()

            add_reactor(react_message)

            await ctx.send("Finished")