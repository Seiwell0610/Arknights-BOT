import discord
from discord.ext import commands
import asyncio

class Disboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mi = 0

    @commands.Cog.listener()
    async def on_message(self, ctx):
        if ctx.content == "!d bump":
            self.mi = ctx.author.id
        if ctx.author.id == 302050872383242240 :
            if "表示順をアップ" in ctx.embeds[0].description:
                mn = self.mi
                msg = await ctx.send(f"<@{mn}>さんBumpを確認しました。\n2時間後に通知します。")
                await asyncio.sleep(10)
                m = 0
                while m < 7201:
                    b = 7200
                    s = b - m
                    await msg.edit(content=f"あと{s}秒後にBumpできます。")
                    await asyncio.sleep(1)
                    m += 1
                await msg.delete()
                await ctx.send(content=f"<@{mn}>\nBump可能")
            
def setup(bot):
    bot.add_cog(Disboard(bot))
