from discord.ext import commands
import os
import importlib.util
import json

mdb_client = commands.Bot(command_prefix='$$')


def get_manifest():
    """
    Loads manifest of modules declared in relevant JSON file
    :return:
    """
    with open("../module/manifest.json") as f:
        manifest = json.load(f)
    print(manifest)
    return manifest


class PluginManager:
    bot = mdb_client
    manifest = get_manifest()

    def __init__(self):
        for x in self.manifest["modules"]:
            spec = importlib.util.spec_from_file_location(x, f"../module/{x}/__module__.py")  # Module file
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)  # Executing module
            print(x)
            print(foo)
            foo.Module(self.bot)  # Running module class

plugin_manager = PluginManager()

