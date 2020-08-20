import discord
from discord.ext import commands
import asyncio
import datetime
import sqlite3
import dropbox

print("auxiliaryの読み込み完了")

dbxtoken = os.environ.get("dbxtoken")
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

class auxiliary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        try:
            await ctx.channel.purge(limit=limit)
            embed = discord.Embed(title="メッセージ削除", description=f"{limit}件のメッセージを削除しました。", color=discord.Color.red())
            await ctx.send(embed=embed)
    
        except:
            embed = discord.Embed(title="メーセージの削除失敗", description="メッセージの削除に失敗しました。", color=discord.Color.dark_red())
            await ctx.send(embed=embed)

    @commands.command()
    async def url(self, ctx, status):
        guild = ctx.guild.id
        conn = sqlite3.connect("all_data_arknights_main.db")
        c = conn.cursor()
        if status == "on":
            c.execute("update settings set url_setting = 1 where guild_id = ?", (guild, ))
            await ctx.send(f"{ctx.author.mention}-> メッセージ展開機能をONにしました。")
        elif status == "off":
            c.execute("update settings set url_setting = 0 where guild_id = ?", (guild, ))
            await ctx.send(f"{ctx.author.mention}-> メッセージ展開機能をOFFにしました。")

        else:
            await ctx.send(f"{ctx.author.mention}-> エラーが発生しました。")

        conn.commit() #変更を保存
        conn.close() #クローズ

        #DropBoxにデータベースをアップロード
        with open("all_data_arknights_main.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data_arknights_main.db", mode=dropbox.files.WriteMode.overwrite)

    
    @commands.command()
    async def report(self, ctx):
        #title
        em1 = discord.Embed(description="タイトルを入力してください",color=0x009193)
        m1 = await ctx.send(embed=em1)
        def check1(m):
            return m.content and m.author == ctx.author
        try:
            titl = await self.bot.wait_for("message",timeout=30.0, check=check1)

        except asyncio.TimeoutError:
            return await ctx.send('タイムアウトしました。')

        else:
            if titl.content != None:
                title = titl.content
                await titl.delete()

        #description
        em2 = discord.Embed(description="報告内容を入力してください",color=0x009193)
        await m1.edit(embed=em2)
        def check2(m):
            return m.content and m.author == ctx.author    
        try:
            dis = await self.bot.wait_for("message",timeout=30.0, check=check2)           
        except asyncio.TimeoutError:
            return await ctx.send('タイムアウトしました。')

        else:
            if dis.content != None:
                disc = dis.content
                await dis.delete()
        
        #送信
        em4 = discord.Embed(title="**バグの報告ありがとうございました**", description="以下の内容で報告いたしました",color=0x009193)
        em4.add_field(name="タイトル", value=f"`{title}`", inline=False)
        em4.add_field(name="内容", value=f"`{disc}`", inline=False)
        await m1.edit(embed=em4)

        em3 = discord.Embed(title=f"**{ctx.author}からのバグレポート**", color=0x009193)
        em3.add_field(name=f"**{title}**", value=f"`{disc}`")
        ch = self.bot.get_channel(int(739094432967688262))
        await ch.send(embed=em3)

        return

def setup(bot):
    bot.add_cog(auxiliary(bot))
