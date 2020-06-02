from discord.ext import commands
import discord
import datetime

class Ninsyo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def _ninsyo(self, ctx):
        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        

def setup(bot):
    bot.add_cog(Ninsyo(bot))
