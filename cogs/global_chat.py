import discord
from discord.ext import commands

class arknights_global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        p = ";"
        if message.author.bot:
            # もし、送信者がbotなら無視する
            return
        GLOBAL_CH_NAME = "arknights-global"  # グローバルチャットのチャンネル名

        if message.channel.name == GLOBAL_CH_NAME:
            # hoge-globalの名前をもつチャンネルに投稿されたので、メッセージを転送する

            await message.delete()  # 元のメッセージは削除しておく

            channels = self.bot.get_all_channels()
            global_channels = [ch for ch in channels if ch.name == GLOBAL_CH_NAME]
            # channelsはbotの取得できるチャンネルのイテレーター
            # global_channelsは hoge-global の名前を持つチャンネルのリスト

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