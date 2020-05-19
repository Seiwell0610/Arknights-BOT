import discord
import sqlite3
from PIL import Image
import io
from discord.ext import commands

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ### アークナイツ/情報表示関連 ###
    @commands.command(name="s")
    async def _s(self, ctx, character):
        #データベース
        character.title()
        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        c.execute('SELECT * FROM character WHERE 名前=?', (character,))
        data = c.fetchone()
        while data is None:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは日本版では実装されていないキャラクターです。",
                                  color=discord.Color.dark_red())
            await ctx.send(embed=embed)
            break
        else:
            embed = discord.Embed(title=f"{data[0]}のデータ:", description=f"{data[1]}", color=0x0096ff)
            embed.add_field(name="職業", value=f"{data[2]}", inline=True)
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name="レア度", value=f"{data[3]}", inline=True)
            embed.add_field(name="HP", value=f"{data[4]}", inline=True)
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name="攻撃力", value=f"{data[5]}", inline=True)
            embed.add_field(name="防御力", value=f"{data[6]}", inline=True)
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name="魔法防御力", value=f"{data[7]}", inline=True)
            embed.add_field(name="再配置", value=f"{data[8]}", inline=True)
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name="配置コスト", value=f"{data[9]}", inline=True)
            embed.add_field(name="ブロック数", value=f"{data[10]}", inline=True)
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name="攻撃速度", value=f"{data[11]}", inline=True)
            embed.add_field(name="募集タグ", value=f"{data[12]}", inline=True)
            embed.add_field(name='\u200b', value='\u200b')
            embed.add_field(name="リンク", value=f"[詳細はこちら](<{data[13]}>)", inline=True)
            embed.set_thumbnail(url=f"{data[14]}")
            await ctx.send(embed=embed)

    @commands.command(name="u")
    async def _u(self, ctx, character):
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

    @commands.command()
    async def tag(self, ctx, character):
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
            await ctx.send(f"{data[11]}")


    @commands.command()
    async def kk(self, ctx, name):
        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()

        tag_split = name.split("/")
        print(tag_split)

        if c.execute('SELECT * FROM character WHERE ? in (タグ1,タグ2,タグ3,タグ4,タグ5)', (tag_split[0],)):
            embed = discord.Embed(title=name, description=None)
            for i in c.execute('SELECT * FROM character WHERE ? in (タグ1,タグ2,タグ3,タグ4,タグ5)', (tag_split[0],)):
                data = c.fetchone()
                data_tag = "/".join(data[1:5])
                i_tag = "/".join(i[1:5])
                embed.add_field(name=data[0], value=f"{data_tag}")
                embed.add_field(name=i[0], value=f"{i_tag}")
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="エラー", description="選択されたタグが間違っているか、該当のキャラクターが\n存在しません。")
            await ctx.send(embed=embed)

    ### カスタム絵文字関連 ###
    @commands.command(name="add_emoji", aliases=["addemoji", "aemoji"])
    async def _add_emoji(self, ctx, *, triger):
        img = ctx.ctx.attachments[0]
        resize = False
        if len(await img.read()) >= 25600:
            im = Image.open(io.BytesIO(await img.read()))
            img_resize = im.resize((350, 350))
            bytesio = io.BytesIO()
            img_resize.save(bytesio, format="PNG")
            resize = True
        if resize == False:
            msg = "カスタム絵文字を追加しました。"
            await ctx.guild.create_custom_emoji(name=triger, image=await img.read())
        else:
            msg = "カスタム絵文字を追加しました。\n絵文字の容量がDiscordの制限を超えていたため、\n自動でリサイズしました。"
            await ctx.guild.create_custom_emoji(name=triger, image=bytesio.getvalue())
        embed = discord.Embed(title="完了！", description=f"{ctx.author.mention}\n{msg}", color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def cleanup(self, ctx):
        await ctx.channel.purge()
        embed = discord.Embed(title="メッセージの削除完了", description="すべてのメッセージを正常に削除しました。", color=discord.Color.blue())
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def 通知(self, ctx):
        role = discord.utils.get(ctx.guild.roles, name='メンションOK')
        if ctx.author.bot:
            return
        if ctx.channel.id == 708503714713043004:
            if role in ctx.author.roles:
                embed = discord.Embed(title="役職の剥奪", description=f"{ctx.author.mention}\n役職：`{role}`を剥奪しました。",
                                      color=discord.Color.dark_blue())
                await ctx.channel.send(embed=embed)
                await ctx.author.remove_roles(role)
            else:
                embed = discord.Embed(title="役職の追加", description=f"{ctx.author.mention}\n役職：`{role}`を付与しました。",
                                     color=discord.Color.dark_blue())
                await ctx.channel.send(embed=embed)
                await ctx.author.add_roles(role)
        else:
            embed = discord.Embed(title="エラー", description="このチャンネルでは、このコマンドは実行できません。",
                                  color=discord.Color.dark_red())
            await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Member(bot))
