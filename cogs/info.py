import discord
from discord.ext import commands
from datetime import datetime


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='info', pass_context=True, hidden=True)
    async def helps(self, ctx):
        invite = "https://discordapp.com/api/oauth2/authorize?client_id=688553944661754054&permissions=379968&scope=bot"
        url = "https://discord.gg/25yrUVp"
        timestamp = datetime.utcfromtimestamp(int(self.bot.user.created_at.timestamp()))
        embed = discord.Embed(title="このBOTのヘルプ:", description=f">>> ```アークナイツに関する情報を表示したり、\n他にも様々な機能を提供します。```[このBOTの招待はこちら](<{invite}>)\n[Arknights JP[Unofficial]サーバーはこちら](<{url}>)", timestamp=timestamp, color=0x009193)
        embed.set_thumbnail(url=self.bot.user.avatar_url)
        embed.add_field(name="導入サーバー数", value=f"`{len(self.bot.guilds)}`")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="総ユーザー数", value=f"`{len(set(self.bot.get_all_members()))}`")
        embed.add_field(name="開発言語", value="`discord.py`")
        embed.add_field(name='\u200b', value='\u200b')
        embed.add_field(name="応答速度", value=f"`{self.bot.ws.latency * 1000:.0f}ms`")
        embed.set_footer(text="このBOTの作成日")
        return await ctx.send(embed=embed)
        ### データを送信 ###
        channel = self.bot.get_channel(676716174087684126)
        embed = discord.Embed(title=f"コマンド実行", description=f"{message.author.mention}\n`{p}info`コマンドの実行",
                              color=discord.Color.blue())
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
