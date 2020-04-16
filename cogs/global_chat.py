import discord
from discord.ext import commands
import sqlite3
import random
import re

class arknights_global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        GLOBAL_WEBHOOK_NAME = "Arknights-webhook"

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        GLOBAL_CH_ID = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_ID.append(row[0])
        print(GLOBAL_CH_ID)
        if message.channel.id in GLOBAL_CH_ID:

            if message.content.startswith(";"):
                pass

            else:
                channels = self.bot.get_all_channels()
                global_channels = [ch for ch in channels if ch.id == GLOBAL_CH_ID]
                for ch in channels:
                    print(ch.id)
                for channel in global_channels:
                    ch_webhooks = await channel.webhooks()
                    webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)

                    if webhook is None:
                        await message.channel.create_webhook(name=GLOBAL_WEBHOOK_NAME)
                        continue
                    if message.attachments:
                        MSG = message.attachments[0].url
                        embed = discord.Embed(title="画像送信", description=" ", color=discord.Color.blue())
                        embed.set_image(url=MSG)
                        await webhook.send(content=message.content, embed=embed, username=message.author.name,
                                           avatar_url=message.author.avatar_url_as(format="png"))
                        return
                    else:
                        await message.delete()
                        await webhook.send(content=message.content, username=message.author.name,
                                           avatar_url=message.author.avatar_url_as(format="png"))
                        return

def setup(bot):
    bot.add_cog(arknights_global(bot))
