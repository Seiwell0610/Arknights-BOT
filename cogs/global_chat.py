import discord
from discord.ext import commands
import sqlite3

class arknights_global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        GLOBAL_WEBHOOK_NAME = message.guild.neme

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        GLOBAL_CH_ID = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_ID.append(row[0])

        if message.channel.id in GLOBAL_CH_ID:

            if message.content.startswith(";"):
                pass

            else:

                await message.delete()

                channels = self.bot.get_all_channels()
                global_channels = [ch for ch in channels if ch.id == GLOBAL_CH_ID]

                for channel in global_channels:
                    ch_webhooks = await channel.webhooks()
                    webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)

                    if webhook is None:
                        continue

                    await webhook.send(content=message.content,
                                       username=message.author.name,
                                       avatar_url=message.author.avatar_url_as(format="png"))

def setup(bot):
    bot.add_cog(arknights_global(bot))