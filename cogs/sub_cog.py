import discord
from discord.ext import commands

class sub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.bot.get_channel(689987791127576753)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="サーバー新規参加", description=f"{member.mention}さん\nサーバー参加ありがとうございます:grinning:\nこのサーバーのことを拡散・宣伝してもらえると嬉しいです:sunglasses:",
                                  color=discord.Color.blue())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(689987791127576753)

        if member.guild.id == 689263691669176426:
            embed = discord.Embed(title="サーバーから退出", description=f"{member.mention}さんがサーバーから退出しました。",color=discord.Color.purple())
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(696206234168328192)
        embed = discord.Embed(title="参加", description=f"`{guild}`に参加しました。",color=discord.Color.blue())
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(696206234168328192)
        embed = discord.Embed(title="脱退", description=f"`{guild}`に脱退しました。",color=discord.Color.dark_red())
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):

        role = discord.utils.get(message.guild.roles, name='Notification')
        if message.author.bot:
            return

        #通知
        if message.content.startswith(";通知"):
            if message.channel.id == 689279925030486045:
                if role in message.author.roles:
                    embed = discord.Embed(title="役職の剥奪", description=f"{message.author.mention}\n役職：`{role}`を剥奪しました。",
                                          color=discord.Color.dark_blue())
                    await message.channel.send(embed=embed)
                    await message.author.remove_roles(role)
                else:
                    embed = discord.Embed(title="役職の追加", description=f"{message.author.mention}\n役職：`{role}`を付与しました。",
                                          color=discord.Color.dark_blue())
                    await message.channel.send(embed=embed)
                    await message.author.add_roles(role)
            else:
                embed = discord.Embed(title="エラー", description="このチャンネルでは、このコマンドは実行できません。",
                                      color=discord.Color.dark_red())
                await message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(sub(bot))
