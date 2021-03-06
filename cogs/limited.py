import discord
from discord.ext import commands

print("limitedの読み込み完了")

class limited(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 689263691669176426:

            ms=len(member.guild.members)
            await member.guild.edit(name=f'ドクター達の集いの場+{ms}人')

            if member.bot:
                return

            await self.bot.get_channel(748752955712208966).send(f"{member}さんが参加しました！")

            em = discord.Embed(title="参加", color=discord.Color.blue())
            em.add_field(name="ユーザー名", value=f"{member}", inline=True)
            em.add_field(name='\u200b', value='\u200b')
            em.add_field(name="ユーザーID", value=f"{member.id}", inline=True)
            await self.bot.get_channel(748747685032493096).send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id == 689263691669176426:

            ms=len(member.guild.members)
            await member.guild.edit(name=f'ドクター達の集いの場+{ms}人')

            if member.bot:
                return

            em = discord.Embed(title="退出", color=discord.Color.purple())
            em.add_field(name="ユーザー名", value=f"{member}", inline=True)
            em.add_field(name='\u200b', value='\u200b')
            em.add_field(name="ユーザーID", value=f"{member.id}", inline=True)
            await self.bot.get_channel(748747685032493096).send(embed=em)

def setup(bot):
    bot.add_cog(limited(bot))
