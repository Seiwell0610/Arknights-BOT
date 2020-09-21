import discord
from discord.ext import commands
import sqlite3
import asyncio
import datetime
import dropbox
from cogs import admin
import r
import os

print("serring_gcの読み込み完了")

self_id=688553944661754054

admin_list = admin.admin_list

dbxtoken = os.environ.get("dbxtoken")
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

ng_content = ["@everyone", "@here"]
GLOBAL_WEBHOOK_NAME = "Arknights-webhook"  # グローバルチャットのウェブフック名

conn = sqlite3.connect('all_data_arknights_main.db')
c = conn.cursor()

class setting_global_chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_global")
    @commands.has_permissions(manage_guild=True)
    async def _add_global(self, ctx):
        ch_id = int(ctx.channel.id)
        guild_id = int(ctx.guild.id)

        c.execute("insert into global_chat (guild_id, channel_id) values (?, ?)", (guild_id, ch_id, ))
        conn.commit()
        await ctx.send(f"{ctx.author.mention}-> グローバルチャットに登録しました。")

        with open("all_data_arknights_main.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data_arknights_main.db", mode=dropbox.files.WriteMode.overwrite)

        embed = discord.Embed(title="グローバルチャット[登録]", description=None, color=discord.Color.blue())
        embed.add_field(name=f"GUILD", value=f"{ctx.guild.name}", inline=False)
        embed.add_field(name="GUILD ID", value=f"{ctx.guild.id}", inline=False)
        embed.add_field(name="CHANNEL", value=f"{ctx.channel.name}", inline=False)
        embed.add_field(name="CHANNEL ID", value=f"{ctx.channel.id}", inline=False)
        channel = self.bot.get_channel(739387932061859911)
        await channel.send(embed=embed)

    @commands.command(name="del_global")
    @commands.has_permissions(manage_guild=True)
    async def _del_global(self, ctx):
        ch_id = int(ctx.channel.id)
        c.execute('DELETE FROM global_chat WHERE channel_id = ?', (ch_id, ))
        conn.commit()

        await ctx.send(f"{ctx.author.mention}-> グローバルチャットの登録を解除しました。")

        with open("all_data_arknights_main.db", "rb") as fc:
            dbx.files_upload(fc.read(), "/all_data_arknights_main.db", mode=dropbox.files.WriteMode.overwrite)

        embed = discord.Embed(title="グローバルチャット[解除]", description=None, color=discord.Color.dark_red())
        embed.add_field(name=f"GUILD", value=f"{ctx.guild.name}", inline=False)
        embed.add_field(name="GUILD ID", value=f"{ctx.guild.id}", inline=False)
        embed.add_field(name="CHANNEL", value=f"{ctx.channel.name}", inline=False)
        embed.add_field(name="CHANNEL ID", value=f"{ctx.channel.id}", inline=False)
        channel = self.bot.get_channel(739387932061859911)
        await channel.send(embed=embed)
        
def setup(bot):
    bot.add_cog(setting_global_chat(bot))
