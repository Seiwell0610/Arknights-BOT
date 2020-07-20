import r
from discord.ext import commands,tasks
import asyncio
import datetime

print("disboardの読み込み完了")
conn=r.connect()

class Disboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.disb.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        dib = conn.get('disboard')
        if message.content == "!d bump":
            dib = int(dib)
            if dib == 'none':
                dib = conn.set('disboard',message.author.id)
                ch = conn.set('channel',message.channel.id)
            else:
                return
        if message.author.id == 302050872383242240:
            if "表示順をアップしたよ" in message.embeds[0].description:
                now = datetime.datetime.now()
                how = now.hour
                miw = now.minute
                if how <= 21:
                    how += 2
                else:
                    how += -22
                await message.channel.send(f"<@{dib}>さんBumpを確認しました。\n2時間後({how}:{miw})に通知します。")
                time = f'{how}{miw}'
                time = conn.set('timer',time)
                
        if message.content.startswith('youtube'):
            if message.author.id == 159985870458322944:
                say = message.content
                url = say.strip('youtube ')
                channel = self.bot.get_channel(714589443373269042)
                await channel.send(url)

    @tasks.loop(seconds=10)
    async def disb(self):
        now = datetime.datetime.now().strftime('%H%M')
        time = conn.get('timer')
        time = int(time)
        now = int(now)
        print(now)
        if now >= time:
            dib = conn.get('disboard')
            ch = conn.get('channel')
            ch = self.bot.get_channel(int(ch))
            await ch.send(f'<@{dib}>さん\n Bump出来るようになりました')
            dib = conn.set('disboard','none')

def setup(bot):
    bot.add_cog(Disboard(bot))
