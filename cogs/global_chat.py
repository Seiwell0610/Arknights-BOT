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

        GLOBAL_WEBHOOK_NAME = "Arknights-webhook"

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        GLOBAL_CH_ID = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_ID.append(row[0])
        
        if message.channel.id in GLOBAL_CH_ID:

            if message.content.startswith(";"):
                pass

            else:
                channels = self.bot.get_all_channels()
                global_channels = [ch for ch in channels if ch.id in GLOBAL_CH_ID]
                for channel in global_channels:
                    ch_webhooks = await channel.webhooks()
                    webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)
                    print(webhook)
                    if webhook is None:
                        await message.channel.create_webhook(name=GLOBAL_WEBHOOK_NAME)
                        continue
                    if message.attachments:
                        if channel.id == message.channel.id:
                            return
                        dcount = 0
                        for p in message.attachments:
                            dcount += 1
                            filenames = filename + f"{dcount}.png"
                            await p.save(f"{filenames}")
                            await webhook.send(file=discord.File(filenames), username=message.author.name,
                                               avatar_url=message.author.avatar_url_as(format="png"))
                           
                    else:
                        await webhook.send(content=message.content, username=message.author.name,
                                           avatar_url=message.author.avatar_url_as(format="png"))
                        if channel.id == message.channel.id:
                            await message.delete()
                        
def setup(bot):
    bot.add_cog(arknights_global(bot))


