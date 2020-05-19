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
        print(data)

        promotion = data[3].split("/")
        hp = data[4].split("/") #HP
        attack = data[5].split("/") #攻撃力
        defense = data[6].split("/") #防御力
        magic_defense = data[7].split("/") #術耐性
        cost = data[9].split("/") #配置コスト
        block = data[10].split("/") #ブロック数

        while data is None:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは既に実装されているキャラクターです。",
                                    color=discord.Color.dark_red())
            await ctx.send(embed=embed)
            break
        else:
            try:
                if len(promotion) == 4:

                    pages = [
                        discord.Embed(title=f"{data[0]}({promotion[0]})のデータ：", color=0x0096ff),
                        discord.Embed(title=f"{data[0]}({promotion[1]})のデータ：", color=0x0096ff),
                        discord.Embed(title=f"{data[0]}({promotion[2]})のデータ：", color=0x0096ff),
                        discord.Embed(title=f"{data[0]}({promotion[3]})のデータ：", color=0x0096ff)
                    ]
                    #ページ1
                    pages[0].add_field(name="職業", value=f"{data[1]}")
                    pages[0].add_field(name="レア度", value=f"{data[2]}")
                    pages[0].add_field(name="HP(信頼度)", value=f"{hp[0]}")
                    pages[0].add_field(name="攻撃力(信頼度)", value=f"{attack[0]}")
                    pages[0].add_field(name="防御力(信頼度)", value=f"{defense[0]}")
                    pages[0].add_field(name="術耐性", value=f"{magic_defense[0]}")
                    pages[0].add_field(name="再配置速度", value=f"{data[8]}")
                    pages[0].add_field(name="配置コスト", value=f"{cost[0]}")
                    pages[0].add_field(name="ブロック数", value=f"{block[0]}")
                    pages[0].add_field(name="攻撃速度", value=f"{data[11]}")
                    pages[0].add_field(name="募集タグ", value=f"{data[12]}")
                    pages[0].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                    pages[0].set_thumbnail(url=f"{data[14]}")

                    # ページ2
                    pages[1].add_field(name="職業", value=f"{data[1]}")
                    pages[1].add_field(name="レア度", value=f"{data[2]}")
                    pages[1].add_field(name="HP(信頼度)", value=f"{hp[1]}")
                    pages[1].add_field(name="攻撃力(信頼度)", value=f"{attack[1]}")
                    pages[1].add_field(name="防御力(信頼度)", value=f"{defense[1]}")
                    pages[1].add_field(name="術耐性", value=f"{magic_defense[1]}")
                    pages[1].add_field(name="再配置速度", value=f"{data[8]}")
                    pages[1].add_field(name="配置コスト", value=f"{cost[1]}")
                    pages[1].add_field(name="ブロック数", value=f"{block[1]}")
                    pages[1].add_field(name="攻撃速度", value=f"{data[11]}")
                    pages[1].add_field(name="募集タグ", value=f"{data[12]}")
                    pages[1].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                    pages[1].set_thumbnail(url=f"{data[14]}")

                    # ページ3
                    pages[2].add_field(name="職業", value=f"{data[1]}")
                    pages[2].add_field(name="レア度", value=f"{data[2]}")
                    pages[2].add_field(name="HP(信頼度)", value=f"{hp[2]}")
                    pages[2].add_field(name="攻撃力(信頼度)", value=f"{attack[2]}")
                    pages[2].add_field(name="防御力(信頼度)", value=f"{defense[2]}")
                    pages[2].add_field(name="術耐性", value=f"{magic_defense[2]}")
                    pages[2].add_field(name="再配置速度", value=f"{data[8]}")
                    pages[2].add_field(name="配置コスト", value=f"{cost[2]}")
                    pages[2].add_field(name="ブロック数", value=f"{block[2]}")
                    pages[2].add_field(name="攻撃速度", value=f"{data[11]}")
                    pages[2].add_field(name="募集タグ", value=f"{data[12]}")
                    pages[2].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                    pages[2].set_thumbnail(url=f"{data[14]}")

                    # ページ4
                    pages[3].add_field(name="職業", value=f"{data[1]}")
                    pages[3].add_field(name="レア度", value=f"{data[2]}")
                    pages[3].add_field(name="HP(信頼度)", value=f"{hp[3]}")
                    pages[3].add_field(name="攻撃力(信頼度)", value=f"{attack[3]}")
                    pages[3].add_field(name="防御力(信頼度)", value=f"{defense[3]}")
                    pages[3].add_field(name="術耐性", value=f"{magic_defense[3]}")
                    pages[3].add_field(name="再配置速度", value=f"{data[8]}")
                    pages[3].add_field(name="配置コスト", value=f"{cost[3]}")
                    pages[3].add_field(name="ブロック数", value=f"{block[3]}")
                    pages[3].add_field(name="攻撃速度", value=f"{data[11]}")
                    pages[3].add_field(name="募集タグ", value=f"{data[12]}")
                    pages[3].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                    pages[3].set_thumbnail(url=f"{data[14]}")

                    nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, timeout=10)
                    nav.start()
                    await ctx.send(nav)

                elif len(promotion) == 3:
                    pages = [
                        discord.Embed(title=f"{data[0]}({promotion[0]})のデータ：", color=0x0096ff),
                        discord.Embed(title=f"{data[0]}({promotion[1]})のデータ：", color=0x0096ff),
                        discord.Embed(title=f"{data[0]}({promotion[2]})のデータ：", color=0x0096ff)
                    ]

                    # ページ1
                    pages[0].add_field(name="職業", value=f"{data[1]}")
                    pages[0].add_field(name="レア度", value=f"{data[2]}")
                    pages[0].add_field(name="HP(信頼度)", value=f"{hp[0]}")
                    pages[0].add_field(name="攻撃力(信頼度)", value=f"{attack[0]}")
                    pages[0].add_field(name="防御力(信頼度)", value=f"{defense[0]}")
                    pages[0].add_field(name="術耐性", value=f"{magic_defense[0]}")
                    pages[0].add_field(name="再配置速度", value=f"{data[8]}")
                    pages[0].add_field(name="配置コスト", value=f"{cost[0]}")
                    pages[0].add_field(name="ブロック数", value=f"{block[0]}")
                    pages[0].add_field(name="攻撃速度", value=f"{data[11]}")
                    pages[0].add_field(name="募集タグ", value=f"{data[12]}")
                    pages[0].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                    pages[0].set_thumbnail(url=f"{data[14]}")

                    # ページ2
                    pages[1].add_field(name="職業", value=f"{data[1]}")
                    pages[1].add_field(name="レア度", value=f"{data[2]}")
                    pages[1].add_field(name="HP(信頼度)", value=f"{hp[1]}")
                    pages[1].add_field(name="攻撃力(信頼度)", value=f"{attack[1]}")
                    pages[1].add_field(name="防御力(信頼度)", value=f"{defense[1]}")
                    pages[1].add_field(name="術耐性", value=f"{magic_defense[1]}")
                    pages[1].add_field(name="再配置速度", value=f"{data[8]}")
                    pages[1].add_field(name="配置コスト", value=f"{cost[1]}")
                    pages[1].add_field(name="ブロック数", value=f"{block[1]}")
                    pages[1].add_field(name="攻撃速度", value=f"{data[11]}")
                    pages[1].add_field(name="募集タグ", value=f"{data[12]}")
                    pages[1].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                    pages[1].set_thumbnail(url=f"{data[14]}")

                    # ページ3
                    pages[2].add_field(name="職業", value=f"{data[1]}")
                    pages[2].add_field(name="レア度", value=f"{data[2]}")
                    pages[2].add_field(name="HP(信頼度)", value=f"{hp[2]}")
                    pages[2].add_field(name="攻撃力(信頼度)", value=f"{attack[2]}")
                    pages[2].add_field(name="防御力(信頼度)", value=f"{defense[2]}")
                    pages[2].add_field(name="術耐性", value=f"{magic_defense[2]}")
                    pages[2].add_field(name="再配置速度", value=f"{data[8]}")
                    pages[2].add_field(name="配置コスト", value=f"{cost[2]}")
                    pages[2].add_field(name="ブロック数", value=f"{block[2]}")
                    pages[2].add_field(name="攻撃速度", value=f"{data[11]}")
                    pages[2].add_field(name="募集タグ", value=f"{data[12]}")
                    pages[2].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                    pages[2].set_thumbnail(url=f"{data[14]}")

                    nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, timeout=10)
                    nav.start()
                    await ctx.send(nav)

                elif len(promotion) == 2:
                    pages = [
                        discord.Embed(title=f"{data[0]}({promotion[0]})のデータ：", color=0x0096ff),
                        discord.Embed(title=f"{data[0]}({promotion[1]})のデータ：", color=0x0096ff)
                    ]

                    # ページ1
                    pages[0].add_field(name="職業", value=f"{data[1]}")
                    pages[0].add_field(name="レア度", value=f"{data[2]}")
                    pages[0].add_field(name="HP(信頼度)", value=f"{hp[0]}")
                    pages[0].add_field(name="攻撃力(信頼度)", value=f"{attack[0]}")
                    pages[0].add_field(name="防御力(信頼度)", value=f"{defense[0]}")
                    pages[0].add_field(name="術耐性", value=f"{magic_defense[0]}")
                    pages[0].add_field(name="再配置速度", value=f"{data[8]}")
                    pages[0].add_field(name="配置コスト", value=f"{cost[0]}")
                    pages[0].add_field(name="ブロック数", value=f"{block[0]}")
                    pages[0].add_field(name="攻撃速度", value=f"{data[11]}")
                    pages[0].add_field(name="募集タグ", value=f"{data[12]}")
                    pages[0].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                    pages[0].set_thumbnail(url=f"{data[14]}")

                    # ページ2
                    pages[1].add_field(name="職業", value=f"{data[1]}")
                    pages[1].add_field(name="レア度", value=f"{data[2]}")
                    pages[1].add_field(name="HP(信頼度)", value=f"{hp[1]}")
                    pages[1].add_field(name="攻撃力(信頼度)", value=f"{attack[1]}")
                    pages[1].add_field(name="防御力(信頼度)", value=f"{defense[1]}")
                    pages[1].add_field(name="術耐性", value=f"{magic_defense[1]}")
                    pages[1].add_field(name="再配置速度", value=f"{data[8]}")
                    pages[1].add_field(name="配置コスト", value=f"{cost[1]}")
                    pages[1].add_field(name="ブロック数", value=f"{block[1]}")
                    pages[1].add_field(name="攻撃速度", value=f"{data[11]}")
                    pages[1].add_field(name="募集タグ", value=f"{data[12]}")
                    pages[1].add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
                    pages[1].set_thumbnail(url=f"{data[14]}")

                    nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, timeout=10)
                    nav.start()
                    await ctx.send(nav)

            except asyncio.TimeoutError:
                pass


def setup(bot):
    bot.add_cog(Character_Search(bot))