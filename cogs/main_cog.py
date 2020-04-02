import discord
import pandas as pd
from PIL import Image
import io
from discord.ext import commands

class Member(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        p = ";"
        if message.author.bot:
            return

        if message.content.startswith(f"{p}s "):
            data = pd.read_csv("data.csv")
            name = message.content.split()[1]
            name_df = data.query('名前== @name')
            if name_df.empty:
                embed = discord.Embed(title="エラー", description="アークナイツに存在しないキャラクター、もしくは日本版では実装されていないキャラクターです。",
                                      color=discord.Color.dark_red())
                await message.channel.send(embed=embed)

            else:
                wiki_link = name_df["リンク"].iloc[0]
                embed = discord.Embed(title=f"{name}のデータ:", color=0x0096ff)
                for key in name_df.keys()[1:12]:
                    embed.add_field(name=f"{key}", value=f"{name_df[key].iloc[0]}", inline=True)
                embed.add_field(name=f"リンク", value=f"[詳細はこちら](<{wiki_link}>)", inline=True)
                await message.channel.send(embed=embed)

    @commands.command(aliases=["addemoji", "aemoji"])
    @commands.has_permissions(manage_emojis=True)
    async def add_emoji(self, ctx, *, triger):
        img = ctx.message.attachments[0]
        resize = False
        if len(await img.read()) >= 25600:
            im = Image.open(io.BytesIO(await img.read()))
            img_resize = im.resize((350, 350))
            bytesio = io.BytesIO()
            img_resize.save(bytesio, format="PNG")
            resize = True
        if resize == False:
            msg = "絵文字を追加しました。"
            await ctx.guild.create_custom_emoji(name=triger, image=await img.read())
        else:
            msg = "絵文字を追加しました。絵文字の容量がDiscordの制限を超えていたため、\n自動でリサイズしました。"
            await ctx.guild.create_custom_emoji(name=triger, image=bytesio.getvalue())
        embed = discord.Embed(title="完了！", description=f"{ctx.author.mention}\n{msg}", color=discord.Color.blue())
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Member(bot))