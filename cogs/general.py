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


def setup(bot):
    bot.add_cog(GeneralCog(bot))
