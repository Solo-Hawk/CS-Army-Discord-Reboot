from discord.ext import commands
from discord.ext import commands as discord


def run_bot():
    bot = commands.Bot(command_prefix='$$')

    @bot.listen("on_ready")
    async def ready():
        guild = bot.get_guild(435616811602673688)
        print(guild.roles)
        role = guild.get_role()

        pass
    


    return bot
