import discord
from discord.ext import commands
import libneko
import sqlite3
from cogs import admin
import r

print("main_programの読み込み完了")

admin_list = admin.admin_list

conn = sqlite3.connect("all_data_arknights_main.db")
c = conn.cursor()

def default_buttons():
    from libneko.pag.reactionbuttons import (
        first_page,
        back_10_pages,
        previous_page,
        next_page,
        forward_10_pages,
        last_page
    )

    return (
        first_page(),
        back_10_pages(),
        previous_page(),
        next_page(),
        forward_10_pages(),
        last_page()
    )
buttons = default_buttons()

class main_program(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="s")
    async def _s(self, ctx, character=None):
        if ctx.author.id not in admin_list:
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['0', '3']
            if pp not in q:
                embed = discord.Embed(title="メンテナンス中", description="現在、メンテナンス中のため使用できません。\nメンテナンスが終わるまでお待ちください。",
                                      color=discord.Color.dark_red())
                return await ctx.send(embed=embed)

        if character is None:
            embed = discord.Embed(title="エラー", description="キャラクター名を指定して下さい。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        character.title()

        c.execute('SELECT * FROM character WHERE 名前=?', (character,))
        data = c.fetchone()

        while data is None:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは日本版では実装されていないキャラクターです。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        else:
            promotion = data[3].split("/")
            hp = data[4].split("/")  # HP
            attack = data[5].split("/")  # 攻撃力
            defense = data[6].split("/")  # 防御力
            magic_defense = data[7].split("/")  # 術耐性
            cost = data[9].split("/")  # 配置コスト
            block = data[10].split("/")  # ブロック数

            pages = []

            for count in range(int(len(promotion))):
                pages.append(discord.Embed(title=f"{data[0]}({promotion[count]})", color=0x0096ff))
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

            nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, buttons=default_buttons(), timeout=10)
            nav.start()
            await ctx.send(nav)

    @commands.command(name="skill")
    async def _skill(self, ctx, character=None):
        if ctx.author.id not in admin_list:
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['0', '3']
            if pp not in q:
                embed = discord.Embed(title="メンテナンス中", description="現在、メンテナンス中のため使用できません。\nメンテナンスが終わるまでお待ちください。",
                                      color=discord.Color.dark_red())
                return await ctx.send(embed=embed)


        c.execute('SELECT * FROM character_skill WHERE 名前=?', (character,))
        data = c.fetchone()

        if character is None:
            embed = discord.Embed(title="エラー", description="キャラクター名を指定して下さい。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        while data is None:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは日本版では実装されていないキャラクターです。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        else:

            quality_name = data[2].split("/")
            quality = data[3].split("/")
            skill_name = data[4].split("/")
            skill = data[5].split("/")
            base_skill_name = data[6].split("/")
            base_skill_conditions = data[7].split("/")
            base_skill_target = data[8].split("/")
            base_skill_effect = data[9].split("/")

            pages = [
                (discord.Embed(title=f"{character}", color=discord.Color.orange())),
                (discord.Embed(title=f"{character}(素質)", color=discord.Color.orange())),
                (discord.Embed(title=f"{character}(スキル)", color=discord.Color.orange())),
                (discord.Embed(title=f"{character}(基地スキル)", color=discord.Color.orange()))
                 ]

            pages[0].add_field(name=f"特性", value=f"{data[1]}\n", inline=False)

            for count in range(int(len(quality_name))):
                pages[1].add_field(name=f"{quality_name[count]}", value=f"{quality[count]}\n", inline=False)

            for count in range(int(len(skill_name))):
                pages[2].add_field(name=f"{skill_name[count]}", value=f"{skill[count]}", inline=False)

            for count in range(int(len(base_skill_name))):
                pages[3].add_field(name=f"{base_skill_name[count]}", value=f"{base_skill_effect[count]}", inline=False)
                pages[3].add_field(name=f"習得条件", value=f"{base_skill_conditions[count]}", inline=True)
                pages[3].add_field(name=f"効果対象", value=f"{base_skill_target[count]}", inline=True)

            nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, buttons=default_buttons(), timeout=10)
            nav.start()
            await ctx.send(nav)

    @commands.command()
    async def stage(self, ctx, stage_number=None):
        if ctx.author.id not in admin_list:
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['0', '3']
            if pp not in q:
                embed = discord.Embed(title="メンテナンス中", description="現在、メンテナンス中のため使用できません。\nメンテナンスが終わるまでお待ちください。",
                                      color=discord.Color.dark_red())
                return await ctx.send(embed=embed)

        c.execute('SELECT * FROM stage WHERE ステージ番号=?', (stage_number,))
        data = c.fetchone()

        if stage_number is None:
            embed = discord.Embed(title="エラー", description="ステージを指定してください。\n例えば：`;stage 1-1`",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        while data is None:
            embed = discord.Embed(title="エラー", description="存在しないステージまたは、指定のステージのデータがありません。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        else:
            embed = discord.Embed(title=f"{data[1]}/{data[0]}", color=discord.Color.green())
            embed.set_image(url=data[3])
            await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(main_program(bot))
