# Author: Davis#9654
import json
import re

import discord


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

            emoji_id_search = re.search(r'^<:([a-zA-Z0-9_.-]+):(\d+)>$', emoji)  # if its not unicode it is discord emoji so we parse string to get id
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

    async def yes_no(self, ctx, prompt):
        def check(reaction, user):
            return ctx.author.id == user.id and reaction.emoji in ['👎', '👍']

        msg = await ctx.send(prompt)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        reaction = await self.bot.wait_for('reaction_add', check=check, timeout=60)
        if reaction[0].emoji == '👍':
            return True
        else:
            return False

    async def get_response(self, ctx, prompt):
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(prompt)
        return (await self.bot.wait_for('message', check=check, timeout=60)).content

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

    def get_prefix(self, bot, message):
        """Returns prefix for bot, currently this allows for changing prefix in future could implement per-server
        prefix"""
        return self.get_guild_data()[str(message.guild.id)]["prefix"]

    @staticmethod
    def reload_guild_data():
        with open('core/guild_data.json') as r:
            return json.load(r)
