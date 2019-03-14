import json
from discord.ext import commands


def load_config():
    with open('core/configs.json') as r:
        return json.load(r)


def update_config(new_config):
    with open('core/configs.json', 'w') as w:
        json.dump(new_config, w)


def has_auth():
    config = load_config()

    def predicate(ctx):
        return ctx.message.author.id in config["auth_ids"]

    return commands.check(predicate)
