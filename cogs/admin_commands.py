import discord
import dropbox
import sqlite3
from discord.ext import commands

dbxtoken = "_Qobiq7UxdAAAAAAAAAAVwmGwxNRDjQuXNSmgwP6N8dqq9umopY2xvaDsc1saAJJ"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

admin_list = []
conn = sqlite3.connect("all_data.db")
c = conn.cursor()
for row in c.execute("SELECT * FROM admin_list"):
    admin_list.append(row[0])
print(admin_list)

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def news(self, ctx, title, main, channel_id=None):
        if ctx.author.id in admin_list:

            if channel_id==None:
                channel_id=ctx.channel.id

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
            conn = sqlite3.connect("all_data.db")
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

def setup(bot):
    bot.add_cog(Member(bot))
