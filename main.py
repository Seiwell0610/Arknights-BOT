import json
import discord
import dropbox
import asyncio
import traceback
from discord.ext import commands

with open('setting.json', mode='r', encoding='utf-8') as fh:
    json_txt = fh.read()
    json_txt = str(json_txt).replace("'", '"').replace('True', 'true').replace('False', 'false')
    token = json.loads(json_txt)['token']
    prefix = json.loads(json_txt)['prefix']
loop = asyncio.new_event_loop()

dbxtoken = "_Qobiq7UxdAAAAAAAAAAUSQMe2MDJyrmNyMWglSKGrfZKrrzGx_ruooafYposH3L"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

async def run():
    bot = MyBot()
    try:
        await bot.start(token)
    except KeyboardInterrupt:
        await bot.logout()

class MyBot(commands.Bot):
    def __init__(self, command_prefix):
        super().__init__(command_prefix, loop=loop)
        self.remove_command('help')

    async def on_ready(self):
        for extension in ["admin", "help", "url", "log", "global_chat", "main_program", "disboard", "limited", "auxiliary"]:
            try:
                self.load_extension(f"cogs.{extension}")
            except commands.ExtensionAlreadyLoaded:
                self.reload_extension(f"cogs.{extension}")


        await self.change_presence(activity=discord.Game(name=f"{prefix}help | {len(self.guilds)}guilds"))

    async def on_guild_join(self, _):
        await self.change_presence(activity=discord.Game(name=f"{prefix}help | {len(self.guilds)}guilds"))

    async def on_guild_remove(self, _):
        await self.change_presence(activity=discord.Game(name=f"{prefix}help | {len(self.guilds)}guilds"))

    async def on_command_error(self, ctx, error1):
        if isinstance(error1, (commands.CommandNotFound, commands.CommandInvokeError)):
            return

if __name__ == '__main__':
    try:
        print("Logged in as")
        with open("all_data_arknights_main.db", "wb") as f:
            metadata, res = dbx.files_download(path="/all_data_arknights_main.db")
            f.write(res.content)
        print("データベースのダウンロード完了")

        main_task = loop.create_task(run())
        loop.run_until_complete(main_task)
        loop.close()
        bot = MyBot(command_prefix=prefix)

        @bot.event
        async def on_command(ctx):
            ch = bot.get_channel(714615013968576572)
            url = ctx.author.avatar_url_as(format=None, static_format='png', size=1024)
            embed = discord.Embed(title="コマンドログ", description="", color=0x00fa9a)
            embed.add_field(name="コマンド実行者", value=f"{ctx.author.name}(ID:{ctx.author.id})", inline=False)
            embed.add_field(name="実行したコマンド", value=f"{ctx.command.name}")
            embed.add_field(name="サーバー", value=f"{ctx.guild.name}(ID:{ctx.guild.id})")
            embed.add_field(name="実行文", value=f"{ctx.message.content}")
            embed.set_thumbnail(url=url)
            embed.timestamp = ctx.message.created_at
            await ch.send(embed=embed)

    except Exception as error:
        print("エラー情報\n" + traceback.format_exc())
