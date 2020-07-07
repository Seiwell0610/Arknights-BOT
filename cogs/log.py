import discord
from discord.ext import commands

main_guild_id = 689263691669176426

class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(696206234168328192)
        embed = discord.Embed(title="参加", description=f"`{guild}`に参加しました。", color=discord.Color.blue())
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(696206234168328192)
        embed = discord.Embed(title="脱退", description=f"`{guild}`に脱退しました。", color=discord.Color.dark_red())
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(log(bot))
