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
        self.upload.start()

    @tasks.loop(seconds=30)
    async def upload(self):
        print("アップロード処理開始")
        with open(UPLOADPATH_LOCAL, "rb") as f:
            dbx.files_upload(f.read(), UPLOADPATH_DBX)
        print("アップロード処理完了")

def setup(bot):
    bot.add_cog(dropbox(bot))
