import discord
from discord.ext import commands
from datetime import datetime
from cogs import admin_commands
import r
import libneko

print("helpの読み込み完了")

admin_list = admin.admin_list

def default_buttons():
    from libneko.pag.reactionbuttons import (
        first_page,
        back_10_pages,
        previous_page,
        next_page,
        forward_10_pages,
        last_page
    )

    return (
        first_page(),
        back_10_pages(),
        previous_page(),
        next_page(),
        forward_10_pages(),
        last_page()
    )
buttons = default_buttons()

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        if ctx.invoked_subcommand is None:

            pages = [(discord.Embed(title="このBOTのヘルプ:", description=f">>> ```アークナイツに関する情報を表示したり、\n他にも様々な機能を提供します。```[このBOTの招待はこちら](<{invite}>)\n[「ドクター達の集いの場」サーバーはこちら](<{url}>)", timestamp=timestamp, color=0x009193)),
                     (discord.Embed(title="基本コマンド", color=discord.Color.blue())),
                     (discord.Embed(title="キャラクター検索", color=discord.Color.blue())),
                     (discord.Embed(title="グローバルチャット", color=discord.Color.blue())),
                     (discord.Embed(title="補助コマンド", color=discord.Color.blue()))
                     ]

            if ctx.author.id in admin_list:
                pages.append(discord.Embed(title="運営専用コマンド", color=discord.Color.blue()))

                pages[4].add_field(name=";admin_list", value="Adminに登録されているIDを表示します。", inline=False)
                pages[4].add_field(name=";;global_chat", value="登録されているグローバルチャットを表示します。", inline=False)
                pages[4].add_field(name=";all_guilds", value="このBOTが参加しているGuildを表示します。", inline=False)
                pages[4].add_field(name=";get_user <ユーザーID>", value="`<ユーザーID>`で指定したユーザーの概要を表示します。", inline=False)
                pages[4].add_field(name=";db_update", value="データベースを最新のものに更新します。", inline=False)
                pages[4].add_field(name=";webhook_reset", value="グローバルチャットに登録しているチャンネルのwebhookをリセットします。\nメンテナンスモードに移行してからしようして下さい。", inline=False)
                
            invite = "https://discord.com/api/oauth2/authorize?client_id=688553944661754054&permissions=1614146624&scope=bot"
            url = "https://discord.gg/25yrUVp"
            pages[0].set_thumbnail(url=self.bot.user.avatar_url)
            pages[0].add_field(name="導入サーバー数", value=f"`{len(self.bot.guilds)}`")
            pages[0].add_field(name='\u200b', value='\u200b')
            pages[0].add_field(name="総ユーザー数", value=f"`{len(set(self.bot.get_all_members()))}`")
            pages[0].add_field(name="開発言語", value="`discord.py`")
            pages[0].add_field(name='\u200b', value='\u200b')
            pages[0].add_field(name="応答速度", value=f"`{self.bot.ws.latency * 1000:.0f}ms`")
            pages[0].set_footer(text="このBOTの作成日")
                
            pages[1].add_field(name=";about", value="このBOTの概要を表示します。", inline=False)
            pages[1].add_field(name=";help", value="コマンド一覧を表示します。", inline=False)
            pages[1].add_field(name=";help <コマンド>", value="`<コマンド>`で指定したコマンドの詳細を表示します。", inline=False)

            pages[2].add_field(name=";s <キャラクター名>", value="`<キャラクター名>`の基本的なスペック(情報)を表示します、", inline=False)
            pages[2].add_field(name=";skill <キャラクター名>", value="`<キャラクター名>`の特性・素質・スキルを表示します。", inline=False)
            pages[2].add_field(name=";tag <キャラクター名>", value="`<キャラクター名>`の募集タグを表示します。", inline=False)

            pages[3].add_field(name=";add_global", value="グローバルチャットに登録します。", inline=False)
            pages[3].add_field(name=";del_global", value="グローバルチャットの登録を解除します。", inline=False)

            pages[4].add_field(name=";add_emoji <絵文字名>", value="画像と一緒に`<絵文字名>`で指定した名前で、カスタム絵文字を追加します。", inline=False)
            pages[4].add_field(name=";cleanup", value="全てのメッセージを削除します。\n※全て削除できない場合があります。", inline=False)

            nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, buttons=default_buttons(), timeout=20)
            nav.start()
            await ctx.send(nav)
            
    @help.command(name="mainte")
    async def _mainte(self, ctx):
        embed=discord.Embed(title="`;meinte <モード>`のヘルプ", description="0：通常モード\n1：グローバルチャット以外停止\n2：グローバルチャットを含め停止\n3：グローバルチャットのみ停止", color=discord.Color.blue())
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))