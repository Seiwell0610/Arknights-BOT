import dropbox
from discord.ext import tasks, commands

dbxtoken = "_Qobiq7UxdAAAAAAAAAAVwmGwxNRDjQuXNSmgwP6N8dqq9umopY2xvaDsc1saAJJ"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()
UPLOADPATH_LOCAL = "data.csv"
UPLOADPATH_DBX = "/data.csv"

class dropbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def upload(self, ctx):
        print("アップロード処理を開始")
        with open("data.csv", "rb") as f:
            print("ファイルの読み込み完了")
            dbx.files_upload(f.read(),UPLOADPATH_DBX,mode=dropbox.files.WriteMode.overwrite)
            print("アップロード処理完了")

def setup(bot):
    bot.add_cog(dropbox(bot))
