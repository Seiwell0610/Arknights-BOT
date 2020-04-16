import discord
from discord.ext import commands
import sqlite3
import random

class arknights_global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        GLOBAL_WEBHOOK_NAME = "Arknights-webhook"

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        GLOBAL_CH_ID = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_ID.append(row[1])

        if message.channel.id in GLOBAL_CH_ID:

            if message.content.startswith(";"):
                return

            else:
                channels = self.bot.get_all_channels()
                global_channels = [ch for ch in channels if ch.name == GLOBAL_CH_ID]
                print(global_channels)
                print(GLOBAL_CH_ID)
                for channel in global_channels:
                    ch_webhooks = await channel.webhooks()
                    webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)

                    if webhook is None:
                        await message.channel.create_webhook(name=GLOBAL_WEBHOOK_NAME)
                        continue
                    if message.attachments:
                        MSG = message.attachments[0].url
                        embed = discord.Embed(title="画像送信",description=" ",color = random.choice((0,0x1abc9c,0x11806a,0x2ecc71,0x1f8b4c,0x3498db,0x206694,0x9b59b6,0x71368a,0xe91e63,0xad1457,0xf1c40f,0xc27c0e,0xe67e22,0x95a5a6,0x607d8b,0x979c9f,0x546e7a,0x7289da,0x99aab5)))
                        embed.set_image(url=MSG)   
                        await webhook.send(content=message.content, embed=embed,  username=message.author.name, avatar_url=message.author.avatar_url_as(format="png"))
                        return
                    else:
                        #await message.delete()
                        await webhook.send(content=message.content,
                                           username=message.author.name,
                                           avatar_url=message.author.avatar_url_as(format="png"))
                        return

                await message.channel.send("line31 Error \n https://github.com/Seiwell0610/Arknights-BOT/blob/0471658b5a7c608a7276f00914c891b583258d9c/cogs/global_chat.py#L31 ")
def setup(bot):
    bot.add_cog(arknights_global(bot))
