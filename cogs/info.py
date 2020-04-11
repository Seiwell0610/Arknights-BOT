import discord
from discord.ext import commands
from datetime import datetime


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['info'])
    async def about(self, ctx):
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

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"{ctx.author.mention}-> `;help <コマンド>`と入力してください。")

    @help.command(name="about")
    async def _about(self, ctx):
        embed = discord.Embed(title="`about`のヘルプ；",
                              description="このBOTの概要を表示されます。", color=discord.Color.blue())
        embed.add_field(name="必要な権限", value="なし")
        await ctx.send(embed=embed)

    @help.command(name="s")
    async def _s(self, ctx):
        embed = discord.Embed(title="`;s`のヘルプ；", description="`;s <キャラクター名>`と送信すると、`<キャラクター名>`の基本的な情報が表示\nされます。", color=discord.Color.blue())
        embed.add_field(name="必要な権限", value="なし")
        await ctx.send(embed=embed)

    @help.command(name="add_global")
    async def _add_global(self, ctx):
        embed = discord.Embed(title="`;add_global`のヘルプ；", description="グローバルチャットを使用できるようになります。", color=discord.Color.blue())
        embed.add_field(name="必要な権限", value="サーバー管理")
        await ctx.send(embed=embed)

    @help.command(name="add_emoji")
    async def _add_emoji(self, ctx):
        embed = discord.Embed(title="`;add_emoji`のヘルプ；",
                              description="カスタム絵文字にしたい画像を一緒に`;add_emoji <名前にしたい名前>`と送信\nするとカスタム絵文字を追加できます。", color=discord.Color.blue())
        embed.add_field(name="必要な権限", value="絵文字の管理")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
