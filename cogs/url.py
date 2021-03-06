from discord import Embed
from discord.ext import commands
import re
import sqlite3

print("urlの読み込み完了")

regex_discord_message_url = (
    'https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})'
)


class url(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        guild = message.guild.id
        conn = sqlite3.connect('all_data_arknights_main.db')
        c = conn.cursor()
        c.execute('SELECT url_setting FROM settings WHERE guild_id=?', (guild,))
        data = c.fetchone()
        if data[0] == 0:
            return
        await dispand(message)

async def dispand(message):
    messages = await extract_messsages(message)
    for m in messages:
        if message.content:
            await message.channel.send(embed=compose_embed(m))
        for embed in m.embeds:
            await message.channel.send(embed=embed)


async def extract_messsages(message):
    messages = []
    for ids in re.finditer(regex_discord_message_url, message.content):
        if message.guild.id != int(ids['guild']):
            return
        fetched_message = await fetch_message_from_id(
            guild=message.guild,
            channel_id=int(ids['channel']),
            message_id=int(ids['message']),
        )
        messages.append(fetched_message)
    return messages


async def fetch_message_from_id(guild, channel_id, message_id):
    channel = guild.get_channel(channel_id)
    message = await channel.fetch_message(message_id)
    return message


def compose_embed(message):
    embed = Embed(
        description=message.content,
        timestamp=message.created_at,
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url,
    )
    embed.set_footer(
        text=message.channel.name,
        icon_url=message.guild.icon_url,
    )
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(
            url=message.attachments[0].proxy_url
        )
    return embed


def setup(bot):
    bot.add_cog(url(bot))
