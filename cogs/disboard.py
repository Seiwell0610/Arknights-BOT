import discord
from discord.ext import commands
import asyncio

class Disboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if ctx.author.id == 302050872383242240 :
            if "表示順をアップ" in ctx.embeds[0].description:
                await ctx.send("Bumpを確認しました。2時間後に通知します。")
                await asyncio.sleep(2*60*60)
                await ctx.send("Bump可能通知")
            
def setup(bot):
    bot.add_cog(Disboard(bot))
