import discord
from discord.ext import commands

print("logの読み込み完了")

main_guild_id = 689263691669176426

class log(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(696206234168328192)
        embed = discord.Embed(title="参加", description=f"`{guild}`に参加しました。", color=discord.Color.blue())
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(696206234168328192)
        embed = discord.Embed(title="脱退", description=f"`{guild}`に脱退しました。", color=discord.Color.dark_red())
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        ch = self.bot.get_channel(714615013968576572)
        url = ctx.author.avatar_url_as(format=None, static_format='png', size=1024)
        embed = discord.Embed(title="コマンドログ", description="", color=0x00fa9a)
        embed.add_field(name="コマンド実行者", value=f"{ctx.author.name}(ID:{ctx.author.id})", inline=False)
        embed.add_field(name="実行したコマンド", value=f"{ctx.command.name}")
        embed.add_field(name="サーバー", value=f"{ctx.guild.name}(ID:{ctx.guild.id})")
        embed.add_field(name="実行文", value=f"{ctx.message.content}")
        embed.set_thumbnail(url=url)
        embed.timestamp = ctx.message.created_at
        await ch.send(embed=embed)

def setup(bot):
    bot.add_cog(log(bot))
