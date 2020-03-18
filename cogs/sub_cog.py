import discord
import pandas as pd
from discord.ext import commands

client = discord.Client()

class sub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(689264601006997547)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="サーバー新規参加", description=f"{member.author.mention}さんがサーバーに参加しました。")
            await channel.send(embed=embed)

    @commands.command()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(689264601006997547)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="サーバーから退出", description=f"{member.author.mention}さんがサーバーから退出しました。")
            await channel.send(embed=embed)



def setup(bot):
    bot.add_cog(sub(bot))