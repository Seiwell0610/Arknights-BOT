import discord
import dropbox
import sqlite3
from discord.ext import commands
from cogs import admin_commands
import r

print("global_chatの読み込み完了")

admin_list=admin_commands.admin_list

dbxtoken = "_Qobiq7UxdAAAAAAAAAAVwmGwxNRDjQuXNSmgwP6N8dqq9umopY2xvaDsc1saAJJ"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ### グローバルチャット関連 ###
    @commands.command(name="add_global")
    @commands.has_permissions(manage_guild=True)
    async def _add_global(self, ctx):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            q = ['0','1']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        channel = self.bot.get_channel(698520936374075453)
        ch_id = ctx.channel.id
        ch_name = ctx.channel.name
        guild = ctx.guild.name
        guild_id = ctx.guild.id

        conn = sqlite3.connect('all_data_arknights_main.db')
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS global_chat(id integer PRIMARY KEY, name text NOT NULL)")
        c.execute("insert into global_chat values(?,?)", (ch_id, ch_name))
        conn.commit()
        conn.close()
        await ctx.send(f"{ctx.author.mention}-> グローバルチャットに登録しました。")

        with open("all_data_arknights_main.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data_arknights_main.db", mode=dropbox.files.WriteMode.overwrite)

        embed = discord.Embed(title="グローバルチャット[登録]", description=None, color=discord.Color.blue())
        embed.add_field(name=f"GUILD", value=f"{guild}", inline=False)
        embed.add_field(name="GUILD ID", value=f"{guild_id}", inline=False)
        embed.add_field(name="CHANNEL", value=f"{ch_name}", inline=False)
        embed.add_field(name="CHANNEL ID", value=f"{ch_id}", inline=False)
        await channel.send(embed=embed)

    @commands.command(name="del_global")
    @commands.has_permissions(manage_guild=True)
    async def _del_global(self, ctx):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        channel = self.bot.get_channel(698520936374075453)
        ch_id = ctx.channel.id
        ch_name = ctx.channel.name
        guild = ctx.guild.name
        guild_id = ctx.guild.id

        conn = sqlite3.connect("all_data_arknights_main.db")
        c = conn.cursor()
        c.execute('DELETE FROM global_chat WHERE id = ?', (ch_id,))
        conn.commit()
        conn.close()
        await ctx.send(f"{ctx.author.mention}-> グローバルチャットの登録を解除しました。")

        with open("all_data_arknights_main.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data_arknights_main.db", mode=dropbox.files.WriteMode.overwrite)

        embed = discord.Embed(title="グローバルチャット[解除]", description=None, color=discord.Color.dark_red())
        embed.add_field(name=f"GUILD", value=f"{guild}", inline=False)
        embed.add_field(name="GUILD ID", value=f"{guild_id}", inline=False)
        embed.add_field(name="CHANNEL", value=f"{ch_name}", inline=False)
        embed.add_field(name="CHANNEL ID", value=f"{ch_id}", inline=False)
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Member(bot))
