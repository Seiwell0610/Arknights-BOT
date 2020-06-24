import discord
from discord.ext import commands
import libneko
import sqlite3
from cogs import admin_commands
import r

admin_list=admin_commands.admin_list

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

class Character_Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="s")
    async def _s(self, ctx, character=None):
        if ctx.author.id not in admin_list:
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        channel = self.bot.get_channel(714615013968576572)
        """コマンドログを送信"""
        embed = discord.Embed(title="コマンド実行ログ", color=discord.Color.green())
        embed.set_thumbnail(url=ctx.author.avatar_url_as(format="png"))
        embed.add_field(name="実行コマンド", value=";s", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="検索キャラクター", value=f"{character}", inline=True)
        embed.add_field(name="ユーザー名", value=f"{ctx.author.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="ユーザーID", value=f"{ctx.author.id}", inline=True)
        embed.add_field(name="サーバー名", value=f"{ctx.guild.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="サーバーID", value=f"{ctx.guild.id}", inline=True)
        embed.add_field(name="チャンネル", value=f"{ctx.channel.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="チャンネルID", value=f"{ctx.channel.id}", inline=True)
        await channel.send(embed=embed)

        if character is None:
            embed = discord.Embed(title="エラー", description="キャラクター名を指定して下さい。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        character.title()
        conn = sqlite3.connect("all_data_arknights_main.db")
        c = conn.cursor()
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

    @commands.command(name="u")
    async def _u(self, ctx, character=None):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        channel = self.bot.get_channel(714615013968576572)
        """コマンドログを送信"""
        embed = discord.Embed(title="コマンド実行ログ", color=discord.Color.green())
        embed.set_thumbnail(url=ctx.author.avatar_url_as(format="png"))
        embed.add_field(name="実行コマンド", value=";u", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="検索キャラクター", value=f"{character}", inline=True)
        embed.add_field(name="ユーザー名", value=f"{ctx.author.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="ユーザーID", value=f"{ctx.author.id}", inline=True)
        embed.add_field(name="サーバー名", value=f"{ctx.guild.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="サーバーID", value=f"{ctx.guild.id}", inline=True)
        embed.add_field(name="チャンネル", value=f"{ctx.channel.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="チャンネルID", value=f"{ctx.channel.id}", inline=True)
        await channel.send(embed=embed)

        if character is None:
            embed = discord.Embed(title="エラー", description="キャラクター名を指定して下さい。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        conn = sqlite3.connect("all_data_arknights_main.db")
        c = conn.cursor()
        c.execute('SELECT * FROM unimplemented_character WHERE 名前=?', (character,))
        data = c.fetchone()
        while data is None:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは既に実装されているキャラクターです。",
                                  color=discord.Color.dark_red())
            await ctx.send(embed=embed)
            break
        else:
            embed = discord.Embed(title=f"{data[0]}のデータ:", color=discord.Color.purple())
            embed.add_field(name="職業", value=f"{data[1]}", inline=True)
            embed.add_field(name="レア度", value=f"{data[2]}", inline=True)
            embed.add_field(name="HP", value=f"{data[3]}", inline=True)
            embed.add_field(name="攻撃力", value=f"{data[4]}", inline=True)
            embed.add_field(name="防御力", value=f"{data[5]}", inline=True)
            embed.add_field(name="魔法防御力", value=f"{data[6]}", inline=True)
            embed.add_field(name="再配置", value=f"{data[7]}", inline=True)
            embed.add_field(name="配置コスト", value=f"{data[8]}", inline=True)
            embed.add_field(name="ブロック数", value=f"{data[9]}", inline=True)
            embed.add_field(name="攻撃速度", value=f"{data[10]}", inline=True)
            embed.add_field(name="募集タグ", value=f"{data[11]}", inline=True)
            await ctx.send(embed=embed)




    @commands.command(name="tag")
    async def _tag(self, ctx, character=None):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        channel = self.bot.get_channel(714615013968576572)
        """コマンドログを送信"""
        embed = discord.Embed(title="コマンド実行ログ", color=discord.Color.green())
        embed.set_thumbnail(url=ctx.author.avatar_url_as(format="png"))
        embed.add_field(name="実行コマンド", value=";tag", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="検索キャラクター", value=f"{character}", inline=True)
        embed.add_field(name="ユーザー名", value=f"{ctx.author.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="ユーザーID", value=f"{ctx.author.id}", inline=True)
        embed.add_field(name="サーバー名", value=f"{ctx.guild.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="サーバーID", value=f"{ctx.guild.id}", inline=True)
        embed.add_field(name="チャンネル", value=f"{ctx.channel.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="チャンネルID", value=f"{ctx.channel.id}", inline=True)
        await channel.send(embed=embed)

        if character is None:
            embed = discord.Embed(title="エラー", description="キャラクター名を指定して下さい。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        conn = sqlite3.connect("all_data_arknights_main.db")
        c = conn.cursor()
        c.execute('SELECT * FROM character WHERE 名前=?', (character,))
        data = c.fetchone()
        while data is  None:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは既に実装されているキャラクターです。",
                                  color=discord.Color.dark_red())
            await ctx.send(embed=embed)
            break
        else:
            await ctx.send(f"{data[0]}：\n{data[12]}")

    @commands.command(name="skill")
    async def _skill(self, ctx, character=None):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        channel = self.bot.get_channel(714615013968576572)
        """コマンドログを送信"""
        embed = discord.Embed(title="コマンド実行ログ", color=discord.Color.orange())
        embed.set_thumbnail(url=ctx.author.avatar_url_as(format="png"))
        embed.add_field(name="実行コマンド", value=";skill", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="検索キャラクター", value=f"{character}", inline=True)
        embed.add_field(name="ユーザー名", value=f"{ctx.author.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="ユーザーID", value=f"{ctx.author.id}", inline=True)
        embed.add_field(name="サーバー名", value=f"{ctx.guild.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="サーバーID", value=f"{ctx.guild.id}", inline=True)
        embed.add_field(name="チャンネル", value=f"{ctx.channel.name}", inline=True)
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="チャンネルID", value=f"{ctx.channel.id}", inline=True)
        await channel.send(embed=embed)
        conn = sqlite3.connect("all_data_arknights_main.db")
        c = conn.cursor()
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

            pages = [
                (discord.Embed(title=f"{character}", color=discord.Color.orange())),
                (discord.Embed(title=f"{character}(素質)", color=discord.Color.orange())),
                (discord.Embed(title=f"{character}(スキル)", color=discord.Color.orange()))
                 ]

            pages[0].add_field(name=f"特性", value=f"{data[1]}\n", inline=False)

            for count in range(int(len(quality_name))):
                pages[1].add_field(name=f"{quality_name[count]}", value=f"{quality[count]}\n", inline=False)

            for count in range(int(len(skill_name))):
                pages[2].add_field(name=f"{skill_name[count]}", value=f"{skill[count]}", inline=False)

            nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, buttons=default_buttons(), timeout=10)
            nav.start()
            await ctx.send(nav)

def setup(bot):
    bot.add_cog(Character_Search(bot))
