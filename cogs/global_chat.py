import discord
from discord.ext import commands
import sqlite3
import asyncio
import requests
import datetime

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

        date = datetime.datetime.now()
        filename = f"{date.year}{date.month}{date.day}-{date.hour}{date.minute}{date.second}"
                        
        if message.channel.id in GLOBAL_CH_ID:

            if message.content.startswith(";"):
                pass

            else:

                if not message.attachments:
                    await message.delete()

                else:
                    dcount = 0
                    for p in message.attachments:
                        dcount += 1
                        filenames = filename + f"({dcount}).png"
                        filepath = p.url
                        download_img(filepath, filenames)
                        channel = self.bot.get_channel(699791241134735453)
                        await channel.send(file=discord.File(filenames))

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

                    await asyncio.sleep(5)
                    pcount = 0
                    for c in message.attachments:
                        pcount += 1

                    if pcount > 1:
                        if message.content:
                            for channel in global_channels:
                                await channel.send(embed=embed)
                        dcount = 0
                        for p in message.attachments:
                            dcount += 1
                            filenames = filename + f"({dcount}).png"
                            pembed = discord.Embed(title=None,
                                                  description=None, color=0x00bfff)
                            pembed.set_image(url=f'https://cdn.discordapp.com/attachments/664353316846829568/699791241134735453/{filenames}')
                            pembed.set_author(name=message.author.display_name,
                                             icon_url=message.author.avatar_url_as(format="png"))
                            pembed.set_footer(text=f"From:{message.guild.name}",
                                             icon_url=message.guild.icon_url_as(format="png"))

                            for channel in global_channels:
                                await channel.send(embed=pembed)
                    else:
                        if message.content:
                            dcount = 1
                            filenames = filename + f"({dcount}).png"
                            embed.set_image(url=f'https://cdn.discordapp.com/attachments/664353316846829568/699791241134735453/{filenames}')
                            
                        else:
                            dcount = 1
                            filenames = filename + f"({dcount}).png"
                            embed = discord.Embed(title=None,
                                                  description=None, color=0x00bfff)
                            embed.set_image(url=f'https://cdn.discordapp.com/attachments/664353316846829568/699791241134735453/{filenames}')
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

