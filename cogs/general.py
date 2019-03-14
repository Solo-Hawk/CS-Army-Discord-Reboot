import discord
from discord.ext import commands


class GeneralCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='github', description='Sends link to github repository for bot.')
    async def get_git(self, ctx):
        embed = discord.Embed(title='CS Army Discord Bot',
                              description='GitHub Link for CS Army Discord Bot',
                              url='https://github.com/Solo-Hawk/CS-Army-Discord-Reboot')
        await ctx.send(embed=embed)

    @commands.command(name="steam")
    async def get_steam(self, ctx):
        embed = discord.Embed(title='CS Army Steam Group',
                              description='Join the Steam Group!',
                              url="https://steamcommunity.com/groups/CSArmyNerds")
        embed.set_image(url="https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/4a/4ae5df07e7d149cd6bd64be8ae8b305ed9dc97d4_full.jpg")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(GeneralCog(bot))
