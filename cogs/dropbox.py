import dropbox
from discord.ext import tasks, commands

dbxtoken = "_Qobiq7UxdAAAAAAAAAAVwmGwxNRDjQuXNSmgwP6N8dqq9umopY2xvaDsc1saAJJ"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()

class dropbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.upload.start()

    @tasks.loop(seconds=30)
    async def upload(self):
        print("処理開始(data.csv)")
        with open("data.csv", "rb") as f:
            dbx.files_upload(f.read(), "/data.csv")
        print("アップロード完了(data.csv)")

    @tasks.loop(seconds=30)
    async def upload(self):
        print("処理開始(channel_id)")
        with open("channel_id.txt", "rb") as f:
            dbx.files_upload(f.read(), "/channel_id.txt")
        print("アップロード完了(channel_id)")

def setup(bot):
    bot.add_cog(dropbox(bot))
