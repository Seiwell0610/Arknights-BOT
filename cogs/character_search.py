import discord
from discord.ext import commands
import libneko
import sqlite3


class Character_Search(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="s")
    async def _s(self, ctx, character=None):
        channel = self.bot.get_channel(714615013968576572)
        """コマンドログを送信"""
        embed = discord.Embed(title="コマンド実行ログ", color=discord.Color.green())
        embed.add_field(name="実行コマンド", value="`;s`", inline=False)
        embed.add_field(name="検索キャラクター", value=f"`{character}`", inline=False)
        embed.add_field(name="実行者(ID)", value=f"{ctx.author.name}({ctx.author.id})", inline=False)
        embed.add_field(name="ギルド名(ID)", value=f"{ctx.guild.name}({ctx.guild.id})", inline=False)
        embed.add_field(name="チャンネル名(ID)", value=f"{ctx.channel.name}({ctx.channel.id})", inline=False)
        await channel.send(embed=embed)

        if character==None:
            embed = discord.Embed(title="エラー", description="キャラクター名を指定して下さい。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

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

            nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, timeout=10)
            nav.start()
            await ctx.send(nav)

        else:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは日本版では実装されていないキャラクターです。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)



    @commands.command(name="u")
    async def _u(self, ctx, character=None):
        channel = self.bot.get_channel(714615013968576572)
        """コマンドログを送信"""
        embed = discord.Embed(title="コマンド実行ログ", color=discord.Color.green())
        embed.add_field(name="実行コマンド", value="`;u`", inline=False)
        embed.add_field(name="検索キャラクター", value=f"`{character}`", inline=False)
        embed.add_field(name="実行者(ID)", value=f"{ctx.author.name}({ctx.author.id})", inline=False)
        embed.add_field(name="ギルド名(ID)", value=f"{ctx.guild.name}({ctx.guild.id})", inline=False)
        embed.add_field(name="チャンネル名(ID)", value=f"{ctx.channel.name}({ctx.channel.id})", inline=False)
        await channel.send(embed=embed)

        if character==None:
            embed = discord.Embed(title="エラー", description="キャラクター名を指定して下さい。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        c.execute('SELECT * FROM unimplemented_character WHERE 名前=?', (character,))
        data = c.fetchone()
        while data == None:
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
        channel = self.bot.get_channel(714615013968576572)
        """コマンドログを送信"""
        embed = discord.Embed(title="コマンド実行ログ", color=discord.Color.green())
        embed.add_field(name="実行コマンド", value="`;tag`", inline=False)
        embed.add_field(name="検索キャラクター", value=f"`{character}`", inline=False)
        embed.add_field(name="実行者(ID)", value=f"{ctx.author.name}({ctx.author.id})", inline=False)
        embed.add_field(name="ギルド名(ID)", value=f"{ctx.guild.name}({ctx.guild.id})", inline=False)
        embed.add_field(name="チャンネル名(ID)", value=f"{ctx.channel.name}({ctx.channel.id})", inline=False)
        await channel.send(embed=embed)

        if character==None:
            embed = discord.Embed(title="エラー", description="キャラクター名を指定して下さい。",
                                  color=discord.Color.dark_red())
            return await ctx.send(embed=embed)

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        c.execute('SELECT * FROM character WHERE 名前=?', (character,))
        data = c.fetchone()
        while data == None:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは既に実装されているキャラクターです。",
                                  color=discord.Color.dark_red())
            await ctx.send(embed=embed)
            break
        else:
            await ctx.send(f"{data[0]}：\n{data[12]}")

def setup(bot):
    bot.add_cog(Character_Search(bot))
