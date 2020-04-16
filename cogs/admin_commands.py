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
c.execute('SELECT * FROM admin_list WHERE id = ?', (admin_list,))

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def all_guilds(self, ctx):
        if ctx.author.id not in admin_list:
            await ctx.send("指定のユーザーのみが使用できます。")

        else:
            guilds = self.bot.guilds  # 参加しているすべてのサーバー
            for guild in guilds:
                await ctx.send(guild.name)

    @commands.command()
    async def global_chat(self, ctx):
        if ctx.author.id not in admin_list:
            await ctx.send("指定のユーザーのみが使用できます。")

        else:
            conn = sqlite3.connect("all_data.db")
            c = conn.cursor()
            for data in c.execute('SELECT * FROM global_chat'):
                await ctx.send(data)


def setup(bot):
    bot.add_cog(Member(bot))