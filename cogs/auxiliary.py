import discord
from discord.ext import commands
import asyncio

print("auxiliaryの読み込み完了")

class auciliary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        try:
            await ctx.channel.purge(limit=limit)
            embed = discord.Embed(title="メッセージ削除", color=discord.Color.dark_purple())
            embed.add_field(name="メッセージの削除完了", value=f"{limit}件のメッセージを削除しました。")
            await ctx.send(embed=embed)

            await asyncio.sleep(2)
            await ctx.message.purge(limit=1)

        except:
            embed = discord.Embed(title="Moderation - purge", description="", color=discord.Color.dark_red())
            embed.add_field(name="削除できませんでした。", value="メーセージの削除に失敗しました。")
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(auciliary(bot))
