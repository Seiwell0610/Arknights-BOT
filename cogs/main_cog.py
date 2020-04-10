import discord
import dropbox
import sqlite3
import pandas as pd
from PIL import Image
import io
from discord.ext import commands

dbxtoken = "_Qobiq7UxdAAAAAAAAAAVwmGwxNRDjQuXNSmgwP6N8dqq9umopY2xvaDsc1saAJJ"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def s(self, ctx, character):
        data = pd.read_csv("data.csv")
        name_df = data.query('名前== @character')
        if name_df.empty:
            embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは日本版では実装されていないキャラクターです。",
                                  color=discord.Color.dark_red())
            await ctx.send(embed=embed)

        else:
            wiki_link = name_df["リンク"].iloc[0]
            embed = discord.Embed(title=f"{character}のデータ:", color=0x0096ff)
            for key in name_df.keys()[1:12]:
                embed.add_field(name=f"{key}", value=f"{name_df[key].iloc[0]}", inline=True)
            embed.add_field(name=f"リンク", value=f"[詳細はこちら](<{wiki_link}>)", inline=True)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def add_global(self, ctx):
        ch_id = ctx.channel.id
        ch_name = ctx.channel.name

        conn = sqlite3.connect('all_data.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS global_chat(id integer PRIMARY KEY, name text NOT NULL)")
        c.execute("insert into global_chat values(?,?)", (ch_id, ch_name));
        conn.commit()
        conn.close()
        await ctx.send(f"{ctx.author.mention}-> グローバルチャットに追加しました。 ")

        with open("all_data.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data.db", mode=dropbox.files.WriteMode.overwrite)

    @commands.command(aliases=["addemoji", "aemoji"])
    async def add_emoji(self, ctx, *, triger):
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