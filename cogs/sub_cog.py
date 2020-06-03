import discord
from discord.ext import commands
import os
import r
import datetime

main_guild_id=689263691669176426

class sub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(711611799614783489)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="メンバー新規参加", description=f"{member.mention}さんがサーバーに参加しました。",
                                  color=discord.Color.blue())
            await channel.send(embed=embed)

        if member.guild.id!=main_guild_id:
            return
        if member.bot:
            return
        join_time=datetime.datetime.now()
        join_minute=join_time.minute
        member_id=member.id
        conn=r.connect()
        ps=conn.set(member_id,join_minute)
        print(ps)
        #データベース書き込み(keyをmember_id,valueをjoin_minute)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(689265615516598434)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="サーバーから退出", description=f"{member.mention}さんがサーバーから退出しました。",color=discord.Color.purple())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(696206234168328192)
        embed = discord.Embed(title="参加", description=f"`{guild}`に参加しました。",color=discord.Color.blue())
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(696206234168328192)
        embed = discord.Embed(title="脱退", description=f"`{guild}`に脱退しました。",color=discord.Color.dark_red())
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(sub(bot))
