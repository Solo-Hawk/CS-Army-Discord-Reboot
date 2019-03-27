
import importlib.util
import json
import core.discordClient as discordClient


def main():
    bot = discordClient.run_bot()
    bot.login("NDM5NTc3MTQ4MDM1MDM5MjMz.DkOqVA.zlg1ii2y51OBJmPl1hhkfW2M318")



    #
    # manifest = get_manifest()
    # run_modules(bot, manifest)


def get_manifest():
    """
    Loads manifest of modules declared in relevant JSON file
    :return:
    """
    with open("module/manifest.json") as f:
        manifest = json.load(f)
    print(manifest)
    return manifest


def run_modules(bot, manifest):

    for x in manifest["modules"]:
        spec = importlib.util.spec_from_file_location(x, f"module/{x}/__module__.py")  # Module file
        unit = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(unit)  # Executing module
        print(x)
        print(unit)
        unit.Module(bot)  # Running module class


if __name__ == '__main__':
    main()

