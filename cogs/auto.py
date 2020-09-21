import discord
from discord.ext import commands
import sqlite3

print("autoの読み込み完了")

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

    @commands.command()
    async def on_guild_remove(self, guild):
        c.execute("DELETE FROM settings WHERE guild_id = ?", (guild.id, ))  # サーバー脱退時に、削除
        conn.commit()

def setup(bot):
    bot.add_cog(auto(bot))
