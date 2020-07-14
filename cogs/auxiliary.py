import discord
from discord.ext import commands
import asyncio

print("auxiliaryの読み込み完了")

class auxiliary(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="purge")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, limit: int):
        try:
            await ctx.channel.purge(limit=limit)
            embed = discord.Embed(title="メッセージ削除", description=f"{limit}件のメッセージを削除しました。", color=discord.Color.red())
            await ctx.send(embed=embed)
    
        except:
            embed = discord.Embed(title="メーセージの削除失敗", description="メッセージの削除に失敗しました。", color=discord.Color.dark_red())
            await ctx.send(embed=embed)
    
    @commands.command()
    async def report(self, message):
        #title
        em1 = discord.Embed(description="タイトルを入力してください",color=0x009193)
        await message.channel.send(embed=em1)
        def check1(m):
            return m.content and m.author == message.author    
        try:
            titl = await self.bot.wait_for("message",timeout=30.0, check=check1)

        except asyncio.TimeoutError:
            return await message.channel.send('タイムアウトしました。')

        #description
        em2 = discord.Embed(description="報告内容を入力してください",color=0x009193)
        await message.channel.send(embed=em2)
        def check2(m):
            return m.content and m.author == message.author    
        try:
            dis = await self.bot.wait_for("message",timeout=30.0, check=check2)
            
        except asyncio.TimeoutError:
            return await message.channel.send('タイムアウトしました。')

        #送信
        em3 = discord.Embed(title=f"**{ctx.author}からのバグレポート**", color=0x009193)
        em3.add_field(name=f"{titl.content}", value=f"{dis.content}")
        ch = self.bot.get_channel(731664672222347295)
        await ch.send(embed=em3)
        
        em4 = discord.Embed(title="バグの報告ありがとうございました。", description="以下の内容で報告いたしました。",color=0x009193)
        em4.add_field(name="タイトル", value=f"{titl.content}", inline=False)
        em4.add_field(name="内容", value=f"{dis.content}", inline=False)
        await message.channel.send(embed=em4)
        return

def setup(bot):
    bot.add_cog(auxiliary(bot))
