import discord
from discord.ext import commands
import sqlite3
import asyncio

class arknights_global(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        conn = sqlite3.connect("all_data.db")
        c = conn.cursor()
        GLOBAL_CH_ID = []
        for row in c.execute("SELECT * FROM global_chat"):
            GLOBAL_CH_ID.append(row[0])

        if message.channel.id in GLOBAL_CH_ID:

            if message.content.startswith(";"):
                pass

            else:

                if not message.attachments:
                    await message.delete()

                channels = self.bot.get_all_channels()
                global_channels = [ch for ch in channels if ch.id in GLOBAL_CH_ID]

                if not message.attachments:
                    embed = discord.Embed(title=None,
                                          description=message.content, color=0x00bfff)
                    embed.set_author(name=message.author.display_name,
                                     icon_url=message.author.avatar_url_as(format="png"))
                    embed.set_footer(text=f"From:{message.guild.name}",
                                     icon_url=message.guild.icon_url_as(format="png"))

                else:
                    if message.content:
                        embed = discord.Embed(title=None,
                                              description=message.content, color=0x00bfff)
                        embed.set_image(url=message.attachments[0].url)
                        embed.set_author(name=message.author.display_name,
                                         icon_url=message.author.avatar_url_as(format="png"))
                        embed.set_footer(text=f"From:{message.guild.name}",
                                         icon_url=message.guild.icon_url_as(format="png"))

                    else:
                        embed = discord.Embed(title=None,
                                              description=None, color=0x00bfff)
                        embed.set_image(url=message.attachments[0].url)
                        embed.set_author(name=message.author.display_name,
                                         icon_url=message.author.avatar_url_as(format="png"))
                        embed.set_footer(text=f"From:{message.guild.name}",
                                         icon_url=message.guild.icon_url_as(format="png"))

                    for p in message.attachments:
                        print(p[0].url)
                        #embed.set_image(url=p['url'])

                for channel in global_channels:
                    await channel.send(embed=embed)

                if message.attachments:
                    await asyncio.sleep(1)
                    await message.delete()

def setup(bot):
    bot.add_cog(arknights_global(bot))
