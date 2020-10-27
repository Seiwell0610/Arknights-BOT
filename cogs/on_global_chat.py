import discord
from discord.ext import commands
import sqlite3
import asyncio
import datetime
import dropbox
from cogs import admin
import r
import os

print("on_global_chatの読み込み完了")

self_id=688553944661754054

admin_list = admin.admin_list

ng_word = ["@everyone","@here"]

dbxtoken = os.environ.get("dbxtoken")
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

GLOBAL_WEBHOOK_NAME = "Arknights-webhook"  # グローバルチャットのウェブフック名

conn = sqlite3.connect('all_data_arknights_main.db')
c = conn.cursor()

class on_global_chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return

        date = datetime.datetime.now()
        filename = f"{date.year}{date.month}{date.day}-{date.hour}{date.minute}{date.second}"
        # 画像保存名(基本)を｢年月日-時分秒｣とする。

        GLOBAL_CH_ID = []
        for row in c.execute("SELECT channel_id FROM global_chat"):
            GLOBAL_CH_ID.append(row[0])

        if message.channel.id in GLOBAL_CH_ID:
            # 発言チャンネルidがGLOBAL_CH_IDに入っていたら反応

            if message.content.startswith(";" or ";add_global"):
                return
            # 発言時、頭に｢;｣がついていたらpass
            if message.author.id not in admin_list:
                conn_r = r.connect()
                pp = conn_r.get("maintenance")
                q = ['0', '1']

                if pp not in q:
                    return await message.channel.send("現在、メンテナンス中です")

            msg = message.clean_content

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
                    await channel.create_webhook(name=GLOBAL_WEBHOOK_NAME)
                    # ウェブフックが無ければ作成後、処理は続ける
                    ch_webhooks = await channel.webhooks()
                    # channelのウェブフックを確認
                    webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)
                    # ch_webhooksからGLOBAL_WEBHOOK_NAMEの物を取得            
                
                if message.attachments:
                    # 画像処理
                    if channel.id == message.channel.id:
                        continue

                    # 送信チャンネルが発言チャンネルと同じなら次のループに

                    if message.content:
                        await webhook.send(content=msg, username=message.author.name,
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
                        continue

                    await webhook.send(content=msg, username=message.author.name,
                                       avatar_url=message.author.avatar_url_as(format=kakutyo))
            
            user = await self.bot.fetch_user(self_id)
            await message.add_reaction('\U00002705')
            await asyncio.sleep(1)
            await message.remove_reaction('\U00002705',user)

def setup(bot):
    bot.add_cog(on_global_chat(bot))
