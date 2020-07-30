from discord.ext import commands,tasks
import asyncio
import traceback
import tw

print("Twitterの読み込み完了")

class Twitter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disb.start()

    @commands.command()
    async def twitter(self, ctx, id=None):
        if id == None:
            id = 'ArknightsStaff'
        

def setup(bot):
    bot.add_cog(Twitter(bot))
