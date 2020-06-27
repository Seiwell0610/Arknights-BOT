import discord
import sqlite3
from discord.ext import commands
import r
import os
import dropbox
from cogs import global_chat_webhook
import asyncio

GLOBAL_WEBHOOK_NAME = global_chat_webhook.GLOBAL_WEBHOOK_NAME
global_channels = global_chat_webhook.global_channels

dbxtoken = "_Qobiq7UxdAAAAAAAAAAUSQMe2MDJyrmNyMWglSKGrfZKrrzGx_ruooafYposH3L"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

admin_list = []
conn = sqlite3.connect("all_data_arknights_main.db")
c = conn.cursor()
for row in c.execute("SELECT * FROM admin_list"):
    admin_list.append(row[0])
print(admin_list)

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def db_update(self, ctx):
        if ctx.author.id in admin_list:
            try:
                with open("all_data_arknights_main.db", "wb") as f:
                    metadata, res = dbx.files_download(path="/all_data_arknights_main.db")
                    f.write(res.content)
                await ctx.send(f"{ctx.author.mention}-> データベースの更新が完了しました。")
            except:
                await ctx.send(f"{ctx.author.mention}-> 何らかのエラーが発生しました。")

        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    @commands.command()
    async def news(self, ctx, title, main, channel_id=None):
        if ctx.author.id in admin_list:

            if channel_id==None:
                channel_id=ctx.channel.id
                await ctx.message.delete()

            try:
                embed = discord.Embed(title=f"**{title}**", description=f"{main}")
                channel = self.bot.get_channel(int(channel_id))
                await channel.send(embed=embed)
                if channel_id!=ctx.channel.id:
                    await ctx.send(f"{ctx.author.mention}-> メッセージの送信が完了しました。")

            except:
                await ctx.send(f"{ctx.author.mantion}-> 何らかのエラーが発生しました。")

        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    @commands.command()
    async def all_guilds(self, ctx):
        if ctx.author.id in admin_list:
            guilds = self.bot.guilds  # 参加しているすべてのサーバー
            for guild in guilds:
                await ctx.send(guild.name)

        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    @commands.command()
    async def global_chat(self, ctx):
        if ctx.author.id in admin_list:
            conn = sqlite3.connect("all_data_arknights_main.db")
            c = conn.cursor()
            for data in c.execute('SELECT * FROM global_chat'):
                await ctx.send(data)

        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    @commands.command()
    async def admin_list(self, ctx):
        if ctx.author.id in admin_list:
            admin_list_1 = ",".join(map(str, admin_list))
            embed = discord.Embed(title="現在の管理者情報", description=f"{admin_list_1}", color=discord.Color.blue())
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    @commands.command()
    async def get_user(self, ctx, id):
        if ctx.author.id in admin_list:
            user = await self.bot.fetch_user(int(id))
            embed = discord.Embed(title="該当ユーザー情報", description=None, color=0x39E64B)
            embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
            embed.add_field(name="該当ユーザー名", value=f"{user.name}", inline=False)
            embed.add_field(name="該当タグ情報", value=f"{user.discriminator}", inline=False)
            embed.add_field(name="検索ユーザーID", value=f"{user.id}", inline=False)
            embed.add_field(name="BOT判定", value=f"{user.bot}", inline=False)
            embed.add_field(name="アカウント作成日", value=f"{user.created_at}", inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    @commands.command()
    async def rkey(self, ctx):
        if ctx.author.id in admin_list:
            conn=r.connect()
            ky=conn.keys()
            if ky==None:
                des="None"
            else:
                des=None
            embed = discord.Embed(title="Radis-Key", description=des)
            for i in ky:
                vl=conn.get(i)
                embed.add_field(name=f'key:`{i}`', value=f'value:`{vl}`')
            await ctx.send(embed=embed)

    @commands.command()
    async def rdel(self, ctx, what=None):
        if ctx.author.id in admin_list:
            if what==None:
                return await ctx.send("削除Key指定エラー")
            conn=r.connect()
            d=conn.delete(what)
            await ctx.send(d)

    @commands.command(name="mainte")
    async def mentos(self, ctx, what=None):
        if ctx.author.id in admin_list:
            conn=r.connect()
            if what==None:
                p=conn.get('maintenance')
                return await ctx.send(f'現在のメンテナンスモード：`{p}`')
            if what=="reset":
                p=conn.set('maintenance','0')
                return await ctx.send('通常モードに移行')
            mente=conn.set('maintenance',what)
            if mente == True:
                await ctx.send(f'メンテナンスモードを`{what}`に変更しました')
            else:
                await ctx.send('移行失敗')

    @commands.command()
    async def webhook_reset(self, ctx):
        if ctx.author.id in admin_list:
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['2','3']
            if pp not in q:
                return await ctx.send("現在、仕様できません")
            for channel in global_channels:
                ch_webhooks = await channel.webhooks()
                webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)
                await webhook.delete()
                await asyncio.sleep(2)
                await channel.create_webhook(name=GLOBAL_WEBHOOK_NAME)
            await ctx.send('完了')
                
def setup(bot):
    bot.add_cog(Member(bot))
