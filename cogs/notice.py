import discord
from discord.ext import commands

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        p = ";"

        if message.content.startswith(f"{p}u "):
            channel = self.bot.get_channel(689264492030328911)
            title = message.content.split()[1]
            directly = message.content.split()[2]
            embed = discord.Embed(title=f"{title}", description=f"{directly}", color=discord.Color.blue())
            await channel.send(embed=embed)