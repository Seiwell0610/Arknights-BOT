import dropbox
from discord.ext import tasks, commands

dbxtoken = "_Qobiq7UxdAAAAAAAAAAUSQMe2MDJyrmNyMWglSKGrfZKrrzGx_ruooafYposH3L"
dbx = dropbox.Dropbox(dbxtoken)
dbx.users_get_current_account()
UPLOADPATH_LOCAL = "data.csv"
UPLOADPATH_DBX = "/data.csv"

class dropbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @tasks.loop(seconds=30)
    async def upload(self):
        with open(UPLOADPATH_LOCAL, "rb") as f:
            dbx.files_upload(f.read(),UPLOADPATH_DBX,mode=dropbox.files.WriteMode.overwrite)
        ch = self.bot.get_channel(696551344059973642)
        await ch.send("``UPLOADED``")
        f.close()

def setup(bot):
    bot.add_cog(dropbox(bot))