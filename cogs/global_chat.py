import discord
from discord.ext import commands
import sqlite3
import random
import re
import datetime
import dropbox
from cogs import admin
import r

print("global_chatの読み込み完了")

admin_list = admin.admin_list

dbxtoken = "_Qobiq7UxdAAAAAAAAAAVwmGwxNRDjQuXNSmgwP6N8dqq9umopY2xvaDsc1saAJJ"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

ng_content = ["@everyone", "@here"]
GLOBAL_WEBHOOK_NAME = "Arknights-webhook"  # グローバルチャットのウェブフック名


class global_chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_global")
    @commands.has_permissions(manage_guild=True)
    async def _add_global(self, ctx):
        if ctx.author.id not in admin_list:
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['0', '1']
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
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['0', '3']
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

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        date = datetime.datetime.now()
        filename = f"{date.year}{date.month}{date.day}-{date.hour}{date.minute}{date.second}"
        # 画像保存名(基本)を｢年月日-時分秒｣とする。

        conn = sqlite3.connect("all_data_arknights_main.db")
        c = conn.cursor()
        GLOBAL_CH_ID = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_ID.append(row[0])

        if message.channel.id in GLOBAL_CH_ID:
            # 発言チャンネルidがGLOBAL_CH_IDに入っていたら反応

            if message.content.startswith(";" or ";add_global"):
                return
            # 発言時、頭に｢;｣がついていたらpass
            if message.author.id not in admin_list:
                conn = r.connect()
                pp = conn.get("maintenance")
                q = ['0', '1']
                if pp not in q:
                    return await message.channel.send("現在、メンテナンス中です")

            if message.content in ng_content:
                return await message.delete()

            else:
                channels = self.bot.get_all_channels()
                # ボットの参加する全てのチャンネル取得
                global_channels = [ch for ch in channels if ch.id in GLOBAL_CH_ID]
                # channelsからGLOBAL_CH_IDと合致する物をglobal_channelsに格納
                au = message.author.avatar_url
                if ".gif" in str(au):
                    kakutyo = "gif"
                else:
                    kakutyo = "png"
                if message.attachments:
                    dcount = 0  # dcountには数字
                    for p in message.attachments:
                        dcount += 1
                        if ".gif" in p.filename:
                            await p.save(f"{dcount}.gif")
                        elif ".jpg" in p.filename:
                            await p.save(f"{dcount}.jpg")
                        elif ".png" in p.filename:
                            await p.save(f"{dcount}.png")
                        elif ".mp4" in p.filename:
                            await p.save(f"{dcount}.mp4")
                        elif ".mp3" in p.filename:
                            await p.save(f"{dcount}.mp3")

                for channel in global_channels:
                    # global_channelsから一つずつ取得

                    ch_webhooks = await channel.webhooks()
                    # channelのウェブフックを確認
                    webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)
                    # ch_webhooksからGLOBAL_WEBHOOK_NAMEの物を取得

                    if webhook is None:
                        await message.channel.create_webhook(name=GLOBAL_WEBHOOK_NAME)
                        continue
                    # ウェブフックが無ければ作成後、処理は続ける

                    if message.attachments:
                        # 画像処理
                        if channel.id == message.channel.id:
                            await message.delete()

                        # 送信チャンネルが発言チャンネルと同じならreturn

                        if message.content:
                            await webhook.send(content=message.content, username=message.author.name,
                                               avatar_url=message.author.avatar_url_as(format=kakutyo))

                        dcount = 0  # dcountには数字
                        for p in message.attachments:
                            dcount += 1
                            if ".gif" in p.filename:
                                filenames = f"{dcount}.gif"
                            elif ".jpg" in p.filename:
                                filenames = f"{dcount}.jpg"
                            elif ".png" in p.filename:
                                filenames = f"{dcount}.png"
                            elif ".mp4" in p.filename:
                                filenames = f"{dcount}.mp4"
                            elif ".mp3" in p.filename:
                                filenames = f"{dcount}.mp3"

                            await webhook.send(file=discord.File(filenames), username=message.author.name,
                                               avatar_url=message.author.avatar_url_as(format=kakutyo))

                    else:
                        if channel.id == message.channel.id:
                            await message.delete()

                        await webhook.send(content=message.content, username=message.author.name,
                                           avatar_url=message.author.avatar_url_as(format=kakutyo))


def setup(bot):
    bot.add_cog(global_chat(bot))


