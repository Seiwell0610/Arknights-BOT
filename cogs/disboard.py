import discord
from discord.ext import commands
import asyncio

print("disboardの読み込み完了")

class Disboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.mi = 0

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "!d bump":
            self.mi = message.author.id
        if message.author.id == 302050872383242240:
            if "表示順をアップ" in message.embeds[0].description:
                mn = self.mi
                msg = await message.channel.send(f"<@{mn}>さんBumpを確認しました。\n2時間後に通知します。")
                await asyncio.sleep(10)
                m = 0
                while m < 7201:
                    b = 7200
                    s = b - m
                    await msg.edit(content=f"あと{s}秒後にBumpできます。")
                    await asyncio.sleep(1)
                    m += 1
                await msg.edit(content=f"<@{mn}>さん\nBumpができるようになりました。")

        if message.content.startswith('youtube'):
            if message.author.id == 159985870458322944:
                say = message.content 
                url = say.strip('youtube ')
                channel = self.bot.get_channel(714589443373269042)
                await channel.send(url)
            
def setup(bot):
    bot.add_cog(Disboard(bot))
