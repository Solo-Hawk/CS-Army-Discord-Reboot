from discord.ext import commands
import discord
import json
import re


class BotHelper:
    def __init__(self, bot):
        self.bot = bot
        self.config = self.reload_config()
        self.guild_data = self.reload_guild_data()

    def convert_emoji(self, emoji):
        """Takes an emoji or an id and converts between ID and Emoji/Unicode"""
        if isinstance(emoji, str):
            try:
                emoji.encode('ascii')  # Check if emoji is a unicode char, if it is throws UnicodeEncodeError
            except UnicodeEncodeError:
                return ord(emoji)  # Return the integer representation

            emoji_id_search = re.search(r'^<:hqdefault:(\d+)>$', emoji)  # if its not unicode it is discord emoji so we parse string to get id
            if emoji_id_search.group(1):
                return int(emoji_id_search.group(1))
        elif isinstance(emoji, int):
            try:
                return chr(emoji)  # from int return chr
            except OverflowError:
                return self.bot.get_emoji(emoji)  # else return discord.Emoji

    @staticmethod
    def reload_config():
        with open('core/configs.json') as r:
            return json.load(r)

    def get_config(self):
        return self.config

    def update_config(self):
        with open('core/configs.json', 'w') as w:
            json.dump(self.config, w, indent=4, sort_keys=True)

    def get_guild_data(self):
        return self.guild_data

    def update_guild_data(self):
        with open('core/guild_data.json', 'w') as w:
            json.dump(self.get_guild_data(), w, indent=4, sort_keys=True)

    @staticmethod
    def reload_guild_data():
        with open('core/guild_data.json') as r:
            return json.load(r)