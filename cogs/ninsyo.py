from discord.ext import commands
import discord
import datetime

main_guild_id=689263691669176426

class Ninsyo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="")
    async def _ninsyo(self, ctx):
        if ctx.guild.id!=main_guild_id:
            return
        command_time=datetime.datetime.now()
        command_minute=command_time.minute
        #データベース読み込み
        

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if ctx.guild.id!=main_guild_id:
            return
        if member.bot:
            return
        join_time=datetime.datetime.now()
        join_minute=join_time.minute
        member_id=member.id
        #データベース書き込み

def setup(bot):
    bot.add_cog(Ninsyo(bot))
