import discord
from discord.ext import commands
import libneko
import asyncio
import sqlite3

admin_list = []
conn = sqlite3.connect("all_data.db")
c = conn.cursor()
for row in c.execute("SELECT * FROM admin_list"):
    admin_list.append(row[0])
print(admin_list)

class Character_Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="s")
    async def _s(self, ctx, character):

        character.title()
        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        c.execute('SELECT * FROM character WHERE 名前=?', (character,))
        data = c.fetchone()

        if data is not None:
            promotion = data[3].split("/")
            hp = data[4].split("/")  # HP
            attack = data[5].split("/")  # 攻撃力
            defense = data[6].split("/")  # 防御力
            magic_defense = data[7].split("/")  # 術耐性
            cost = data[9].split("/")  # 配置コスト
            block = data[10].split("/")  # ブロック数

            pages = []

            for count in range(int(len(promotion))):
                pages.append(discord.Embed(title=f"{data[0]}({promotion[count]})"))
                pages[count].add_field(name="職業", value=f"{data[1]}")
                pages[count].add_field(name="レア度", value=f"{data[2]}")
                pages[count].add_field(name="HP(信頼度)", value=f"{hp[count]}")
                pages[count].add_field(name="攻撃力(信頼度)", value=f"{attack[count]}")
                pages[count].add_field(name="防御力(信頼度)", value=f"{defense[count]}")
                pages[count].add_field(name="術耐性", value=f"{magic_defense[count]}")
                pages[count].add_field(name="再配置速度", value=f"{data[8]}")
                pages[count].add_field(name="配置コスト", value=f"{cost[count]}")
                pages[count].add_field(name="ブロック数", value=f"{block[count]}")
                pages[count].add_field(name="攻撃速度", value=f"{data[11]}")
                pages[count].add_field(name="募集タグ", value=f"{data[12]}")
                pages[count].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                pages[count].set_thumbnail(url=f"{data[14]}")
                count += 1

            nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, timeout=10)
            nav.start()
            await ctx.send(nav)

        else:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは日本版では実装されていないキャラクターです。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Character_Search(bot))