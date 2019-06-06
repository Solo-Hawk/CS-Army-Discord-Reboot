from discord.ext import commands
import json
import os


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
                "mod_id": 0
        }

        guild_data_default = {}

        for file, default_value in [(config_file, config_default), (guild_data_file, guild_data_default)]:
            if not os.path.exists(file):
                with open(file, 'w') as w:
                    json.dump(default_value, w)

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
            json.dump(guild_data, w)

    def get_guild_data(self, guild_id, key=None):
        guild_data = self.guild_data()
        if key is None:
            return guild_data[str(guild_id)]
        try:
            return guild_data[str(guild_id)][key]
        except KeyError:
            return None

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

