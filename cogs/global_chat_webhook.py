import discord
from discord.ext import commands
import sqlite3
import random
import re
import datetime

class arknights_global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        date = datetime.datetime.now()
        filename = f"{date.year}{date.month}{date.day}-{date.hour}{date.minute}{date.second}" 
        #画像保存名(基本)を｢年月日-時分秒｣とする。

        GLOBAL_WEBHOOK_NAME = "Arknights-webhook"
        #グローバルチャットのウェブフック名

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        GLOBAL_CH_ID = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_ID.append(row[0])
        
        if message.channel.id in GLOBAL_CH_ID:
        #発言チャンネルidがGLOBAL_CH_IDに入っていたら反応

            if message.content.startswith(";"):
                pass
            #発言時、頭に｢;｣がついていたらpass

            else:
                channels = self.bot.get_all_channels()
                #ボットの参加する全てのチャンネル取得
                global_channels = [ch for ch in channels if ch.id in GLOBAL_CH_ID]
                #channelsからGLOBAL_CH_IDと合致する物をglobal_channelsに格納

                for channel in global_channels:
                #global_channelsから一つずつ取得

                    ch_webhooks = await channel.webhooks()
                    #channelのウェブフックを確認
                    webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)
                    #ch_webhooksからGLOBAL_WEBHOOK_NAMEの物を取得

                    if webhook is None:
                        await message.channel.create_webhook(name=GLOBAL_WEBHOOK_NAME)
                        continue
                    #ウェブフックが無ければ作成後、処理は続ける

                    if message.attachments:
                    #画像処理
                        if channel.id == message.channel.id:
                            return
                        #送信チャンネルが発言チャンネルと同じならreturn
                        if message.content:
                            await webhook.send(content=message.content, username=message.author.name,
                                               avatar_url=message.author.avatar_url_as(format="png"))
                        dcount = 0 #dcountには数字
                        for p in message.attachments:
                            dcount += 1
                            if ".gif" in p.filename:
                                filenames = p.filename
                            elif ".jpg" in p.filename:
                                filenames = filename + f"{dcount}.jpg"
                            elif ".png" in p.filename:
                                filenames = filename + f"{dcount}.png"
                            else:
                                filenames = p.filename #保存名.png 決定
                            await p.save(f"{filenames}") #ローカル保存
                            await webhook.send(file=discord.File(filenames), username=message.author.name,
                                               avatar_url=message.author.avatar_url_as(format="png"))
                           
                    else:
                        if channel.id == message.channel.id:
                            await message.delete()

                        await webhook.send(content=message.content, username=message.author.name,
                                           avatar_url=message.author.avatar_url_as(format="png"))
                        
                        
def setup(bot):
    bot.add_cog(arknights_global(bot))


