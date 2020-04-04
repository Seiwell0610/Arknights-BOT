import discord
from discord.ext import commands
from datetime import datetime


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx):
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

    @commands.command()
    async def help(self, ctx):
        embed = discord.Embed(title="このBOTで使用できる機能:", color=0x942192)
        embed.add_field(name="[コマンド] ;info", value="招待リンクや応答速度などこのBOTの概要について表示します。", inline=False)
        embed.add_field(name="[コマンド] ;c", value="指定されたキャラクターの主なステータスとwikiへのリンクを表示します。", inline=False)
        embed.add_field(name="[コマンド] ;通知", value="一度送信すると通知されるようになります。\nまた、再度送信すると通知されなくなります。", inline=False)
        embed.add_field(name="[機能] グローバルチャット",
                        value="他のサーバーにこのBOTを入れ、「arknights-global」というチャンネル名で\n作成すると、グローバルチャットが使用できます", inline=False)
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
