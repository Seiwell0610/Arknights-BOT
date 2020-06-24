from discord.ext import commands
import discord
import datetime
import r
import os
from cogs import admin_commands

admin_list=admin_commands.admin_list

main_guild_id=689263691669176426
role_name="認証済み"

class Ninsyo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def agree(self, ctx):
        if ctx.author.id not in admin_list:
            conn=r.connect()
            pp=conn.get("maintenance")
            q = ['0','3']
            if pp not in q:
                return await ctx.send("現在、メンテナンス中です")

        if ctx.guild.id!=main_guild_id:
            return
        c=0
        for i in ctx.author.roles:
            if i.name==role_name:
                c=1
        if c==1:
            return await ctx.send("既に、認証しています。")
        command_time=datetime.datetime.now()
        command_minute=command_time.minute
        members=ctx.author.id
        #データベース読み込み(値をjtに)
        conn=r.connect()
        jt=conn.get(members)
        x=int(command_minute)-int(jt)
        if x<0:
            x+=60
        if x>2:
            role = discord.utils.get(ctx.guild.roles,name=role_name)
            await ctx.author.add_roles(role)
            await ctx.send("認証が完了しました。")
            p=conn.delete(members)
            print(p)
        else:
            x=3-x
            await ctx.send(f"後{x}分後に認証ができます。")

def setup(bot):
    bot.add_cog(Ninsyo(bot))
