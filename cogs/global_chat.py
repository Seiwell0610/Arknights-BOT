import discord
from discord.ext import commands
import sqlite3

class arknights_global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            # もし、送信者がbotなら無視する
            return

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        GLOBAL_CH_NAME = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_NAME.append(row[0])

        if message.channel.id == GLOBAL_CH_NAME:

            await message.delete()  # 元のメッセージは削除しておく

            channels = self.bot.get_all_channels()
            global_channels = [ch for ch in channels if ch.id == GLOBAL_CH_NAME]

            embed = discord.Embed(title=message.content,
                                  description=None, color=0x00bfff)

            embed.set_author(name=message.author.display_name,
                             icon_url=message.author.avatar_url_as(format="png"))
            embed.set_footer(text=f"{message.guild.name}",
                             icon_url=message.guild.icon_url_as(format="png"))
            # Embedインスタンスを生成、投稿者、投稿場所などの設定

            for channel in global_channels:
                # メッセージを埋め込み形式で転送
                await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(arknights_global(bot))