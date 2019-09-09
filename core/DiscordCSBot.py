from discord.ext import commands
import json
import os
import discord
import re


class DiscordCSBot(commands.Bot):
    def __init__(self, command_prefix, config_file="core/configs.json", guild_data_file="core/guild_data.json",
                 **options):
        super().__init__(command_prefix, **options)

        self.config_file = config_file
        self.guild_data_file = guild_data_file

        config_default = {
                "auth_ids": [],
                "extensions": [],
                "default_prefix": "$$",
                "mod_id": 0,
                "auth_roles": [],
                "case_category": 0,
                "guild_id": 0,
                "mod_id": 0
        }

        guild_data_default = {}

        for file, default_value in [(config_file, config_default), (guild_data_file, guild_data_default)]:
            if not os.path.exists(file):
                with open(file, 'w') as w:
                    json.dump(default_value, w, indent=4)

    def guild_data(self):
        with open(self.guild_data_file) as r:
            return json.load(r)

    def guild_data_update(self, guild_id, data, append=True):
        """Adds to guild_data, if append is True appends to list if false overwrites"""
        guild_data = self.guild_data()

        if str(guild_id) not in guild_data:
            guild_data[str(guild_id)] = {}

        for data_key, data_value in data.items():
            if isinstance(guild_data.get(data_key), list) and append:
                guild_data[str(guild_id)][data_key].append(data_value)
            else:
                guild_data[str(guild_id)][data_key] = data_value

        with open(self.guild_data_file, 'w') as w:
            json.dump(guild_data, w, indent=4)

    def get_guild_data(self, guild_id, key=None):
        guild_data = self.guild_data()
        if key is None:
            return guild_data[str(guild_id)]
        try:
            return guild_data[str(guild_id)][key]
        except KeyError:
            return None

    def write_guild_data(self, data):
        with open(self.guild_data_file, 'w'):
            json.dump(data, indent=4)

    def get_config(self, config=None):
        with open(self.config_file) as r:
            if config is None:
                return json.load(r)
            try:
                return json.load(r)[config]
            except KeyError as k:
                print("Config Key does not exist " + k)

    def config_update(self, data, append=True):
        """Adds to guild_data, if append is True appends to list if false overwrites"""
        config = self.get_config()

        for data_key, data_value in data.items():
            if isinstance(config.get(data_key), list) and append:
                config[data_key].extend(data_value)
            else:
                config[data_key] = data_value

        with open(self.config_file, 'w') as w:
            json.dump(config, w)

    async def yes_no(self, ctx, prompt):
        def check(reaction, user):
            return ctx.author.id == user.id and reaction.emoji in ['👎', '👍']

        msg = await ctx.send(prompt)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        reaction = await self.wait_for('reaction_add', check=check, timeout=60)
        if reaction[0].emoji == '👍':
            return True
        else:
            return False

    async def get_response(self, ctx, prompt):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(prompt)
        return (await self.wait_for('message', check=check, timeout=60)).content

    def convert_emoji(self, emoji):
        """Takes an emoji or an id and converts between ID and Emoji/Unicode"""
        if isinstance(emoji, str):
            try:
                emoji.encode('ascii')  # Check if emoji is a unicode char, if it is throws UnicodeEncodeError
            except UnicodeEncodeError:
                return ord(emoji)  # Return the integer representation

            emoji_id_search = re.search(r'^<:([a-zA-Z0-9_.-]+):(\d+)>$',
                                        emoji)  # if its not unicode it is discord emoji so we parse string to get id
            if emoji_id_search.group(2):
                return int(emoji_id_search.group(2))
        elif isinstance(emoji, int):
            try:
                return chr(emoji)  # from int return chr
            except OverflowError:
                return self.bot.get_emoji(emoji)  # else return discord.Emoji

    def convert_partial_emoji(self, emoji):
        if isinstance(emoji, discord.PartialEmoji):  # if emoji is a PartialEmoji
            if emoji.is_custom_emoji():  # if custom then we return the id
                return emoji.id
            elif emoji.is_unicode_emoji():  # if unicode then we return int representation
                return ord(emoji.name)
        if isinstance(emoji, str):  # if it is string then we just convert to int
            try:
                emoji = int(emoji)
            except ValueError:
                print("Convert_partial_emoji has been passed a non-int string")
        if isinstance(emoji, int):  # if it is int then we convert to unicode or to discord.Emoji
            try:
                return chr(emoji)  # from int return chr
            except OverflowError:
                return self.bot.get_emoji(emoji)  # else return discord.Emoji

