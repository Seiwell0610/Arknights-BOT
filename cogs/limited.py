import discord
from discord.ext import commands
import os
import datetime
import r
from cogs import admin

main_guild_id = 689263691669176426
role_name="認証済み"
admin_list = admin.admin_list

class limited(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(711611799614783489)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="メンバー新規参加", description=f"{member.mention}さんがサーバーに参加しました。",
                                  color=discord.Color.blue())
            await channel.send(embed=embed)

        if member.guild.id != main_guild_id:
            return
        if member.bot:
            return
        join_time=datetime.datetime.now()
        join_minute=join_time.minute
        member_id=member.id
        conn=r.connect()
        ps=conn.set(member_id, join_minute)
        print(ps)
        #データベース書き込み(keyをmember_id,valueをjoin_minute)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(689265615516598434)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="サーバーから退出", description=f"{member.mention}さんがサーバーから退出しました。", color=discord.Color.purple())
            await channel.send(embed=embed)
            conn = r.connect()
            p = conn.delete(member.id)

    @commands.command()
    async def agree(self, ctx):
        if ctx.author.id not in admin_list:
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['0', '3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        if ctx.guild.id != main_guild_id:
            return
        c = 0
        for i in ctx.author.roles:
            if i.name == role_name:
                c = 1
        if c == 1:
            return await ctx.send("既に、認証しています。")
        command_time = datetime.datetime.now()
        command_minute = command_time.minute
        members = ctx.author.id
        # データベース読み込み(値をjtに)
        conn = r.connect()
        jt = conn.get(members)
        x = int(command_minute) - int(jt)
        if x < 0:
            x += 60
        if x > 2:
            role = discord.utils.get(ctx.guild.roles, name=role_name)
            await ctx.author.add_roles(role)
            await ctx.send("認証が完了しました。")
            p = conn.delete(members)
            print(p)
        else:
            x = 3 - x
            await ctx.send(f"後{x}分後に認証ができます。")

    @commands.command()
    async def 通知(self, ctx):
        if ctx.author.id not in admin_list:
            conn = r.connect()
            pp = conn.get("maintenance")
            q = ['0', '3']
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

def setup(bot):
    bot.add_cog(limited(bot))
