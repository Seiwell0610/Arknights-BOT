from discord.ext import commands,tasks
import asyncio
import traceback

print("disboardの読み込み完了")

class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disb.start()

def setup(bot):
    bot.add_cog(Twitter(bot))
