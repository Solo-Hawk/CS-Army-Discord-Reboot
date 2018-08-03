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

        @bot.listen('on_message')
        async def message_received(message: discord.Message):
            if message.author.bot:
                return
            if not type(message.channel) == discord.DMChannel:
                return
            
            guild = bot.get_guild(472942076003352577)
            channel = await guild.create_text_channel(f"case {message.author.id}", category=self.category)
            await channel.send(f"<@&{self.rolecall}> {message.author.mention}")
            await message.channel.send("This is private DMS")

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



