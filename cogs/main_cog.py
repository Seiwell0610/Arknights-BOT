import discord
import pandas as pd
from discord.ext import commands

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        p = ";"
        if message.author.bot:
            return

        if message.content.startswith(f"{p}cs "):
            data = pd.read_csv("data.csv")
            name = message.content.split()[1]
            name_df = data.query('名前== @name')
            if name_df.empty:
                embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは日本版では実装されていないキャラクターです。",
                                      color=discord.Color.dark_red())
                await message.channel.send(embed=embed)

            else:
                wiki_link = name_df["リンク"].iloc[0]
                embed = discord.Embed(title=f"{name}のデータ:", color=0x0096ff)
                for key in name_df.keys()[1:12]:
                    embed.add_field(name=f"{key}", value=f"{name_df[key].iloc[0]}", inline=True)
                embed.add_field(name=f"リンク", value=f"[詳細はこちら](<{wiki_link}>)", inline=True)
                await message.channel.send(embed=embed)
        if message.content.startswith(f"{p}server_join "):
            channel = self.bot.get_channel(689987791127576753)
            men = message.content.split()[1]
            embed = discord.Embed(title="サーバー新規参加",
                                  description=f"<@{men}>さん\nよろしくお願いします！！！\nこのサーバーのことを拡散・宣伝してもらえると嬉しいです:sunglasses:")
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Member(bot))