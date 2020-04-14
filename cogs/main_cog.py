import discord
import dropbox
import sqlite3
from PIL import Image
import io
from discord.ext import commands

dbxtoken = "_Qobiq7UxdAAAAAAAAAAVwmGwxNRDjQuXNSmgwP6N8dqq9umopY2xvaDsc1saAJJ"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

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
        c.execute('SELECT * FROM character_data WHERE 名前=?', (character,))
        data = c.fetchone()
        while data == None:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは日本版では実装されていないキャラクターです。",
                                  color=discord.Color.dark_red())
            await ctx.send(embed=embed)
            break
        else:
            embed = discord.Embed(title=f"{data[0]}(初期)のデータ:", color=0x0096ff)
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
            embed.add_field(name="リンク", value=f"[詳細はこちら](<{data[12]}>)", inline=True)
            embed.set_thumbnail(url=f"{data[13]}")
            await ctx.send(embed=embed)

    @commands.command(name="u")
    async def _u(self, ctx, character):
        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        c.execute('SELECT * FROM unimplemented_character_data WHERE 名前=?', (character,))
        data = c.fetchone()
        while data == None:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは既に実装されているキャラクターです。",
                                  color=discord.Color.dark_red())
            await ctx.send(embed=embed)
            break
        else:
            embed = discord.Embed(title=f"{data[0]}(初期)のデータ:", color=discord.Color.purple())
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



    ### グローバルチャット関連 ###
    @commands.command(name="add_global")
    @commands.has_permissions(manage_guild=True)
    async def _add_global(self, ctx):
        channel = self.bot.get_channel(698520936374075453)
        ch_id = ctx.channel.id
        ch_name = ctx.channel.name
        guild = ctx.guild.name
        guild_id = ctx.guild.id

        conn = sqlite3.connect('all_data.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS global_chat(id integer PRIMARY KEY, name text NOT NULL)")
        c.execute("insert into global_chat values(?,?)", (ch_id, ch_name));
        conn.commit()
        conn.close()
        await ctx.send(f"{ctx.author.mention}-> グローバルチャットに登録しました。")

        with open("all_data.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data.db", mode=dropbox.files.WriteMode.overwrite)

        embed = discord.Embed(title="グローバルチャット[登録]", description=None, color=discord.Color.blue())
        embed.add_field(name=f"GUILD", value=f"{guild}", inline=False)
        embed.add_field(name="GUILD ID", value=f"{guild_id}", inline=False)
        embed.add_field(name="CHANNEL", value=f"{ch_name}", inline=False)
        embed.add_field(name="CHANNEL ID", value=f"{ch_id}", inline=False)
        await channel.send(embed=embed)

    @commands.command(name="del_global")
    @commands.has_permissions(manage_guild=True)
    async def _del_global(self, ctx):
        channel = self.bot.get_channel(698520936374075453)
        ch_id = ctx.channel.id
        ch_name = ctx.channel.name
        guild = ctx.guild.name
        guild_id = ctx.guild.id

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        c.execute('DELETE FROM global_chat WHERE id = ?', (ch_id,))
        conn.commit()
        conn.close()
        await ctx.send(f"{ctx.author.mention}-> グローバルチャットの登録を解除しました。")

        with open("all_data.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data.db", mode=dropbox.files.WriteMode.overwrite)

        embed = discord.Embed(title="グローバルチャット[解除]", description=None, color=discord.Color.purple())
        embed.add_field(name=f"GUILD", value=f"{guild}", inline=False)
        embed.add_field(name="GUILD ID", value=f"{guild_id}", inline=False)
        embed.add_field(name="CHANNEL", value=f"{ch_name}", inline=False)
        embed.add_field(name="CHANNEL ID", value=f"{ch_id}", inline=False)
        await channel.send(embed=embed)

    ### カスタム絵文字関連 ###
    @commands.command(name="add_emoji", liases=["addemoji", "aemoji"])
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



def setup(bot):
    bot.add_cog(Member(bot))