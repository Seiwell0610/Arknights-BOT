import discord
import sqlite3
from PIL import Image
import io
from discord.ext import commands
from cogs import admin_commands
import r

admin_list=admin_commands.admin_list

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="add_emoji", aliases=["addemoji", "aemoji"])
    async def _add_emoji(self, ctx, *, triger):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            pp=int(pp)
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        img = ctx.ctx.attachments[0]
        resize = False
        if len(await img.read()) >= 25600:
            im = Image.open(io.BytesIO(await img.read()))
            img_resize = im.resize((350, 350))
            bytesio = io.BytesIO()
            img_resize.save(bytesio, format="PNG")
            resize = True
        if resize == False:
            msg = "カスタム絵文字を追加しました。"
            await ctx.guild.create_custom_emoji(name=triger, image=await img.read())
        else:
            msg = "カスタム絵文字を追加しました。\n絵文字の容量がDiscordの制限を超えていたため、\n自動でリサイズしました。"
            await ctx.guild.create_custom_emoji(name=triger, image=bytesio.getvalue())
        embed = discord.Embed(title="完了！", description=f"{ctx.author.mention}\n{msg}", color=discord.Color.blue())
        await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def cleanup(self, ctx):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            pp=int(pp)
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        await ctx.channel.purge()
        embed = discord.Embed(title="メッセージの削除完了", description="すべてのメッセージを正常に削除しました。", color=discord.Color.blue())
        await ctx.channel.send(embed=embed)

    @commands.command()
    async def 通知(self, ctx):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            pp=int(pp)
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        role = discord.utils.get(ctx.guild.roles, name='メンションOK')
        if ctx.author.bot:
            return
        if ctx.channel.id == 708503714713043004:
            if role in ctx.author.roles:
                embed = discord.Embed(title="役職の剥奪", description=f"{ctx.author.mention}\n役職：`{role}`を剥奪しました。",
                                      color=discord.Color.dark_blue())
                await ctx.channel.send(embed=embed)
                await ctx.author.remove_roles(role)
            else:
                embed = discord.Embed(title="役職の追加", description=f"{ctx.author.mention}\n役職：`{role}`を付与しました。",
                                     color=discord.Color.dark_blue())
                await ctx.channel.send(embed=embed)
                await ctx.author.add_roles(role)
        else:
            embed = discord.Embed(title="エラー", description="このチャンネルでは、このコマンドは実行できません。",
                                  color=discord.Color.dark_red())
            await ctx.channel.send(embed=embed)

    @commands.command()
    async def youtube(self, ctx, url):
        if ctx.author.id in admin_list:
            channel = self.bot.get_channel(714589443373269042)
            await channel.send(url)

def setup(bot):
    bot.add_cog(Member(bot))
