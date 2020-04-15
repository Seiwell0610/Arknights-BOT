import discord
from discord.ext import commands
import sqlite3
import asyncio
import requests

def download_img(url, file_name):
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(file_name, 'wb') as f:
            f.write(r.content)

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

                else:
                    filepath = message.attachments[0].url
                    filename = message.attachments[0].filename
                    download_img(filepath, filename)
                    channel = self.bot.get_channel(699791241134735453)
                    await channel.send(file=discord.File(filename))

                channels = self.bot.get_all_channels()
                global_channels = [ch for ch in channels if ch.id in GLOBAL_CH_ID]

                if not message.attachments:
                    embed = discord.Embed(title=None,
                                          description=message.content, color=0x00bfff)
                    embed.set_author(name=message.author.display_name,
                                     icon_url=message.author.avatar_url_as(format="png"))
                    embed.set_footer(text=f"From:{message.guild.name}",
                                     icon_url=message.guild.icon_url_as(format="png"))
                    for channel in global_channels:
                        await channel.send(embed=embed)

                else:
                    if message.content:
                        embed = discord.Embed(title=None,
                                              description=message.content, color=0x00bfff)
                        embed.set_author(name=message.author.display_name,
                                         icon_url=message.author.avatar_url_as(format="png"))
                        embed.set_footer(text=f"From:{message.guild.name}",
                                         icon_url=message.guild.icon_url_as(format="png"))

                    pcount = 0
                    for c in message.attachments:
                        pcount += 1

                    if pcount > 1:
                        if message.content:
                            for channel in global_channels:
                                await channel.send(embed=embed)
                        for p in message.attachments:
                            pembed = discord.Embed(title=None,
                                                  description=None, color=0x00bfff)
                            pembed.set_image(url=p.url)
                            pembed.set_author(name=message.author.display_name,
                                             icon_url=message.author.avatar_url_as(format="png"))
                            pembed.set_footer(text=f"From:{message.guild.name}",
                                             icon_url=message.guild.icon_url_as(format="png"))

                            for channel in global_channels:
                                await channel.send(embed=pembed)
                    else:
                        if message.content:
                            embed.set_image(url=message.attachments[0].url)
                        else:
                            embed = discord.Embed(title=None,
                                                  description=None, color=0x00bfff)
                            embed.set_image(url=message.attachments[0].url)
                            embed.set_author(name=message.author.display_name,
                                             icon_url=message.author.avatar_url_as(format="png"))
                            embed.set_footer(text=f"From:{message.guild.name}",
                                             icon_url=message.guild.icon_url_as(format="png"))
                        for channel in global_channels:
                            await channel.send(embed=embed)
                

                if message.attachments:
                    await asyncio.sleep(1)
                    await message.delete()

def setup(bot):
    bot.add_cog(arknights_global(bot))

