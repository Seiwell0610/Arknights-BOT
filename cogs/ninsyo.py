from discord.ext import commands
import discord
import datetime

class Ninsyo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Ninsyo(bot))
