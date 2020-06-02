from discord.ext import commands
import discord
import datetime
import r

main_guild_id=689263691669176426
role_name="認証完了済み"

class Ninsyo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="arknight")
    async def _ninsyo(self, ctx):
        if ctx.guild.id!=main_guild_id:
            return
        command_time=datetime.datetime.now()
        command_minute=command_time.minute
        members=ctx.author.id
        #データベース読み込み(値をjtに)
        conn=r.connect()
        jt=conn.get(members)
        jt=str(jt)
        x=command_minute-jt
        if x<0:
            x+=60
        if x>4:
            members=self.bot.get_user(members)
            role = discord.utils.get(ctx.guild.roles,name=role_name)
            await members.add_roles(role1)
            await ctx.send("登録しました")
            p=conn.delete(members)
            print(p)
        else:
            x=5-x
            await ctx.send(f"後{x}分後に登録できます")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if ctx.guild.id!=main_guild_id:
            return
        if member.bot:
            return
        join_time=datetime.datetime.now()
        join_minute=join_time.minute
        member_id=member.id
        conn=r.connect()
        ps=conn.set(member_id,join_minute)
        print(ps)
        #データベース書き込み(keyをmember_id,valueをjoin_minute)

def setup(bot):
    bot.add_cog(Ninsyo(bot))
