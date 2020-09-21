import discord
from discord.ext import commands
import sqlite3
import dropbox
import os

print("autoの読み込み完了")

dbxtoken = os.environ.get("dbxtoken")
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

conn = sqlite3.connect('all_data_arknights_main.db')
c = conn.cursor()

class auto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def on_guild_join(self, guild):
        set_number = 1
        c.execute("insert into settings (guild_id, url_setting) values (?, ?)", (guild.id, set_number,)) # settingsのデータベースに新規追加
        conn.commit()
        with open("all_data_arknights_main.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data_arknights_main.db", mode=dropbox.files.WriteMode.overwrite)
        print("データベースに追加")

    @commands.command()
    async def on_guild_remove(self, guild):
        c.execute("DELETE FROM settings WHERE guild_id = ?", (guild.id, ))  # サーバー脱退時に、削除
        conn.commit()
        with open("all_data_arknights_main.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data_arknights_main.db", mode=dropbox.files.WriteMode.overwrite)
        print("データベースに削除")

def setup(bot):
    bot.add_cog(auto(bot))
