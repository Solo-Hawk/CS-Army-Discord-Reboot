# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
# WORK IN PROGRESS MODULE
import discord
from discord.ext import commands
# standard import for any module
import json

auth_roles = {"auth_roles": []}

def get_guild_role(guild: discord.Guild, role: int):
    for role in guild.roles:
        if role.id == role:
            return role
    return

def get_roles():
    with open('auth_roles.json') as json_file:
        auth_roles = json.load(json_file)
    return auth_roles["auth_roles"]


def save_roles():
    with open('auth_roles.json', 'w') as outfile:
        json.dump(auth_roles, outfile)


def add_role(role: str):

    print(role)
    if role in auth_roles["auth_roles"]:
        return
    auth_roles["auth_roles"].append(role)
    save_roles()


def remove_role(role: str):
    print(role)
    auth_roles["auth_roles"].remove(role)
    save_roles()


def is_auth_role(ctx: commands.Context):
    check = False
    for roleid in get_roles():  # Iterator through all auth_roles saved in mdb config
        for role in ctx.author.roles:
            print(role.name)
            print(roleid, "  :  ", role.id)
        if roleid in [role.id for role in ctx.author.roles]:
            return True  # Match found
    return False  # Match NOT found

