import discord
from discord.ext import commands
import sqlite3
import random
import re
import datetime
from cogs import admin_commands
import r

admin_list=admin_commands.admin_list

ng_content = ["@everyone","@here"]
GLOBAL_WEBHOOK_NAME = "Arknights-webhook"#グローバルチャットのウェブフック名

class arknights_global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['p'])
    async def picture(self, ctx, what=None):
        if ctx.author.bot:
            return
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            q = ['0','1']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        conn = sqlite3.connect("all_data_arknights_main.db")
        c = conn.cursor()
        GLOBAL_CH_ID = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_ID.append(row[0])

        file = discord.File(f"picture/{what}.png", filename=f"{what}.png")

        if ctx.channel.id in GLOBAL_CH_ID:
            channels = self.bot.get_all_channels()
            global_channels = [ch for ch in channels if ch.id in GLOBAL_CH_ID]
            for channel in global_channels:
                ch_webhooks = await channel.webhooks()
                webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)
                await webhook.send(file=file, 
                                   username=ctx.author.name,
                                   avatar_url=ctx.author.avatar_url)
        else:
            await ctx.send(file=file)

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author.bot:
            return
        
        date = datetime.datetime.now()
        filename = f"{date.year}{date.month}{date.day}-{date.hour}{date.minute}{date.second}" 
        #画像保存名(基本)を｢年月日-時分秒｣とする。

        conn = sqlite3.connect("all_data_arknights_main.db")
        c = conn.cursor()
        GLOBAL_CH_ID = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_ID.append(row[0])
        
        if message.channel.id in GLOBAL_CH_ID:
        #発言チャンネルidがGLOBAL_CH_IDに入っていたら反応

            if message.content.startswith(";" or ";add_global"):
                return
            #発言時、頭に｢;｣がついていたらpass
            if message.author.id not in admin_list:
                conn=r.connect()
                pp=conn.get("maintenance")
                q = ['0','1']
                if pp not in q:
                    return await message.channel.send("現在、メンテナンス中です")
     

            if message.content in ng_content:
                return await message.delete()

            else:
                channels = self.bot.get_all_channels()
                #ボットの参加する全てのチャンネル取得
                global_channels = [ch for ch in channels if ch.id in GLOBAL_CH_ID]
                #channelsからGLOBAL_CH_IDと合致する物をglobal_channelsに格納
                au=message.author.avatar_url
                if ".gif" in str(au):
                    kakutyo="gif"
                else:
                    kakutyo="png"
                if message.attachments:
                    dcount = 0 #dcountには数字
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
                            await message.delete()
 
                        #送信チャンネルが発言チャンネルと同じならreturn

                        if message.content:
                            await webhook.send(content=message.content, username=message.author.name,
                                               avatar_url=message.author.avatar_url_as(format=kakutyo))

                        dcount = 0 #dcountには数字
                        for p in message.attachments:
                            dcount += 1
                            if ".gif" in p.filename:
                                filenames=f"{dcount}.gif"
                            elif ".jpg" in p.filename:
                                filenames=f"{dcount}.jpg"
                            elif ".png" in p.filename:
                                filenames=f"{dcount}.png"
                            elif ".mp4" in p.filename:
                                filenames=f"{dcount}.mp4"
                            elif ".mp3" in p.filename:
                                filenames=f"{dcount}.mp3"
                            
                            await webhook.send(file=discord.File(filenames), username=message.author.name,
                                               avatar_url=message.author.avatar_url_as(format=kakutyo))
                           
                    else:
                        if channel.id == message.channel.id:
                            await message.delete()
                            
                        await webhook.send(content=message.content, username=message.author.name,
                                           avatar_url=message.author.avatar_url_as(format=kakutyo))
                        
                        
def setup(bot):
    bot.add_cog(arknights_global(bot))


