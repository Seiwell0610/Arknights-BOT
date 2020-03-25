import discord
from discord.ext import commands

class sub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(689987791127576753)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="サーバー新規参加", description=f"{member.mention}さん\nサーバー参加ありがとうございます:grinning:\nこのサーバーのことを拡散・宣伝してもらえると嬉しいです:sunglasses:",
                                  color=discord.Color.blue())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(689987791127576753)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="サーバーから退出", description=f"{member.mention}さんがサーバーから退出しました。",color=discord.Color.purple())
            await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(sub(bot))