from discord import NotFound, Embed, Forbidden
import discord
from discord.ext import commands
import r

import sqlite3
import asyncio
import io
import traceback
import textwrap
import contextlib
import dropbox
import libneko

print("adminの読み込み完了")

GLOBAL_WEBHOOK_NAME = "Arknights-webhook"

dbxtoken = "_Qobiq7UxdAAAAAAAAAAUSQMe2MDJyrmNyMWglSKGrfZKrrzGx_ruooafYposH3L"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

admin_list = []
conn = sqlite3.connect("all_data_arknights_main.db")
c = conn.cursor()
for row in c.execute("SELECT * FROM admin_list"):
    admin_list.append(row[0])

def cleanup_code(content):
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])
    return content.strip('` \n')

def get_syntax_error(e):
    if e.text is None:
        return f'```py\n{e.__class__.__name__}: {e}\n```'
    return f'```py\n{e.text}{"^":>{e.offset}}\n{e.__class__.__name__}: {e}```'

def mention_to_user_id(mention):
    user_id = mention.strip("<@").strip(">")
    if user_id.find("!") != -1:
        user_id = user_id.strip("!")
    return int(user_id)

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

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    #evalコマンド
    @commands.command(name='eval', pass_context=True, description="※運営専用コマンド")
    @commands.bot_has_permissions(read_messages=True, send_messages=True, embed_links=True, add_reactions=True,
                                  manage_messages=True, read_message_history=True)
    async def evals(self, ctx):
        try:
            if ctx.author.id not in admin_list:
                return await ctx.send("指定ユーザーのみが使用できます")

            env = {'bot': self.bot, 'ctx': ctx, 'channel': ctx.channel, 'author': ctx.author, 'guild': ctx.guild,
                   'message': ctx.message, '_': self._last_result}
            env.update(globals())
            body = cleanup_code(ctx.message.content[6:].lstrip())
            stdout = io.StringIO()
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
            try:
                exec(to_compile, env)
            except Exception as e:
                return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
            func = env['func']
            try:
                with contextlib.redirect_stdout(stdout):
                    ret = await func()
            except Exception as _:
                value = stdout.getvalue()
                await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
            else:
                value = stdout.getvalue()
                try:
                    await ctx.message.add_reaction('\u2705')
                except Exception:
                    pass
                if ret is None:
                    if value:
                        await ctx.send(f'```py\n{value}\n```')
                else:
                    self._last_result = ret
                    await ctx.send(f'```py\n{value}{ret}\n```')

        except (NotFound, asyncio.TimeoutError, Forbidden):
            return
        except:
            return print("エラー情報\n" + traceback.format_exc())

    #データベース更新コマンド
    @commands.command()
    async def db_update(self, ctx):
        if ctx.author.id in admin_list:
            try:
                with open("all_data_arknights_main.db", "wb") as f:
                    metadata, res = dbx.files_download(path="/all_data_arknights_main.db")
                    f.write(res.content)
                await ctx.send(f"{ctx.author.mention}-> データベースの更新が完了しました。")
            except:
                await ctx.send(f"{ctx.author.mention}-> 何らかのエラーが発生しました。")

        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    #メンテナンス切り替えコマンド
    @commands.command(name="mainte")
    async def mainte(self, ctx, what=None):
        if ctx.author.id in admin_list:
            conn = r.connect()
            if what == None:
                p = conn.get('maintenance')
                return await ctx.send(f'現在のメンテナンスモード：`{p}`')
            if what == "reset":
                p = conn.set('maintenance', '0')
                return await ctx.send('通常モードに移行')
            mente = conn.set('maintenance', what)
            if mente == True:
                await ctx.send(f'メンテナンスモードを`{what}`に変更しました')
            else:
                await ctx.send('移行失敗')

    #webhookリセットコマンド
    @commands.command()
    async def webhook_reset(self, ctx):
        if ctx.author.id in admin_list:
            # ---メンテモード確認---
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['2','3']
            if pp not in q:
                return await ctx.send("現在、使用できません")
            # -------------------

            # ---embedの生成---
            embed = discord.Embed(title=f"**提供メンテナンス項目**", description=None)
            GLOBAL_CH_ID = []
            for row in c.execute("SELECT * FROM global_chat"):
                GLOBAL_CH_ID.append(row[0])
            channels = self.bot.get_all_channels()
            global_channels = [ch for ch in channels if ch.id in GLOBAL_CH_ID]
            chm=len(global_channels)
            embed.add_field(name=f"webhook更新中", value=f"0/{chm}")
            ky = conn.keys()
            ky = [k for k in ky if k != 'maintenance']
            kys = len(ky)
            embed.add_field(name=f"redis key削除中", value=f"0/{kys}")
            msg = await ctx.send(embed=embed)
            # -------------------

            # ---webhookの再生成---
            m=0
            for channel in global_channels:
                ch_webhooks = await channel.webhooks()
                webhook = discord.utils.get(ch_webhooks, name=GLOBAL_WEBHOOK_NAME)
                await webhook.delete()
                await asyncio.sleep(2)
                await channel.create_webhook(name=GLOBAL_WEBHOOK_NAME)
                m+=1
                embed = discord.Embed(title=f"**提供メンテナンス項目**", description=None)
                embed.add_field(name=f"webhook更新中", value=f"{m}/{chm}")
                embed.add_field(name=f"redis key削除中", value=f"0/{kys}")
                await msg.edit(embed=embed)
            embed = discord.Embed(title=f"**提供メンテナンス項目**", description=None)
            embed.add_field(name=f"webhook更新完了", value=f"{m}/{chm}")
            embed.add_field(name=f"redis key削除中", value=f"0/{kys} \n miss key:[]")
            await msg.edit(embed=embed)
            # -------------------

            # ---redis key再設定---
            n = 0
            msk = []
            for k in ky:
                kye = conn.delete(k)
                if kye == 1:
                    n+=1
                    embed = discord.Embed(title=f"**提供メンテナンス項目**", description=None)
                    embed.add_field(name=f"webhook更新完了", value=f"{m}/{chm}")
                    embed.add_field(name=f"redis key削除中", value=f"{n}/{kys}")
                    await msg.edit(embed=embed)
                else:
                    msk.append(k)
            embed = discord.Embed(title=f"**提供メンテナンス項目**", description=None)
            embed.add_field(name=f"webhook更新完了", value=f"{m}/{chm}")
            embed.add_field(name=f"redis key削除完了", value=f"{n}/{kys} \n miss key:{msk}")
            await msg.edit(embed=embed)
            # -------------------
            return
            #車止め

    #admin表示コマンド
    @commands.command()
    async def admin_list(self, ctx):
        if ctx.author.id in admin_list:
            pages = []
            for count in range(len(admin_list)):
                pages.append(discord.Embed(title="現在の管理者情報", color=discord.Color.blue()))
                user = self.bot.get_user(int(admin_list[count]))
                pages[count].add_field(name="ユーザー名", value=f"{user.name} #{user.discriminator}", inline=False)
                pages[count].add_field(name="ユーザーID", value=f"{admin_list[count]}", inline=False)
            nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, buttons=default_buttons(), timeout=10)
            nav.start()
            await ctx.send(nav)

        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    #登録グローバルチャット表示コマンド
    @commands.command()
    async def global_chat(self, ctx):
        if ctx.author.id in admin_list:
            try:
                pages = []
                global_chat = []
                conn = sqlite3.connect("all_data_arknights_main.db")
                c = conn.cursor()
                for data in c.execute('SELECT * FROM global_chat'):
                    global_chat.append(int(data[0]))

                for count in range(len(global_chat)):
                    pages.append(discord.Embed(title="登録されているチャンネル", color=discord.Color.blue()))
                    channel = self.bot.get_channel(int(global_chat[count]))
                    pages[count].add_field(name="CHANNEL", value=f"{channel}", inline=False)
                    pages[count].add_field(name="CHANNEL ID", value=f"{global_chat[count]}", inline=False)

                nav = libneko.pag.navigator.EmbedNavigator(ctx, pages, buttons=default_buttons(), timeout=10)
                nav.start()
                await ctx.send(nav)


            except:
                print("エラー情報\n" + traceback.format_exc())

        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    #参加サーバー表示コマンド
    @commands.command()
    async def all_guilds(self, ctx):
        if ctx.author.id in admin_list:
            guilds = self.bot.guilds
            for guild in guilds:
                await ctx.send(guild.name)
        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    #ユーザー情報表示コマンド
    @commands.command()
    async def get_user(self, ctx, id):
        if ctx.author.id in admin_list:
            user = await self.bot.fetch_user(int(id))
            embed = discord.Embed(title="該当ユーザー情報", description=None, color=0x39E64B)
            embed.set_thumbnail(url=user.avatar_url_as(static_format="png"))
            embed.add_field(name="該当ユーザー名", value=f"{user.name}", inline=False)
            embed.add_field(name="該当タグ情報", value=f"{user.discriminator}", inline=False)
            embed.add_field(name="検索ユーザーID", value=f"{user.id}", inline=False)
            embed.add_field(name="BOT判定", value=f"{user.bot}", inline=False)
            embed.add_field(name="アカウント作成日", value=f"{user.created_at}", inline=False)
            await ctx.send(embed=embed)

        else:
            await ctx.send(f"{ctx.author.mention}-> 運営専用コマンドです。指定のユーザー以外は実行できません。")

    #サーバー情報表示コマンド
    @commands.command()
    async def get_guild(self, ctx, guild_id: int = None):
        if ctx.author.id in admin_list:
            if guild_id == None:
                guild_id = ctx.guild.id
            guild = self.bot.get_guild(guild_id)
            embed = discord.Embed(title="該当サーバー情報", description=None)
            embed.add_field(name="サーバー名", value=f'`{guild.name}`')
            embed.add_field(name="現オーナー名", value=f'`{guild.owner}`')
            embed.add_field(name="作成日", value=f'`{guild.created_at}`')
            embed.add_field(name="サーバーID", value=f'`{guild.id}`')
            member_count = sum(1 for member in guild.members if not member.bot)
            bot_count = sum(1 for member in guild.members if member.bot)
            all_count = (member_count) + (bot_count)
            embed.add_field(name="総人数", value=f'`{all_count}`', inline=False)
            embed.add_field(name="ユーザ数", value=f'`{member_count}`', inline=False)
            embed.add_field(name="BOT数", value=f'`{bot_count}`', inline=False)
            embed.add_field(name="テキストチャンネル数", value=f'`{len(guild.text_channels)}`', inline=False)
            embed.add_field(name="ボイスチャンネル数", value=f'`{len(guild.voice_channels)}`', inline=False)
            embed.set_thumbnail(url=guild.icon_url)
            await ctx.send(embed=embed)

    #rkey
    @commands.command()
    async def rkey(self, ctx):
        if ctx.author.id in admin_list:
            conn = r.connect()
            ky = conn.keys()
            if ky == None:
                des = "None"
            else:
                des = None
            embed = discord.Embed(title="Radis-Key", description=des)
            for i in ky:
                vl = conn.get(i)
                embed.add_field(name=f'key:`{i}`', value=f'value:`{vl}`')
            await ctx.send(embed=embed)

    #rdel
    @commands.command()
    async def rdel(self, ctx, what=None):
        if ctx.author.id in admin_list:
            if what == None:
                return await ctx.send("削除Key指定エラー")
            conn = r.connect()
            d = conn.delete(what)
            await ctx.send(d)

def setup(bot):
    bot.add_cog(Admin(bot))
