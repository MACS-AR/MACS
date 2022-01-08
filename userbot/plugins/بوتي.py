from userbot import jmthon
from userbot.utils import admin_cmd

from ..Config import Config


@jmthon.on(admin_cmd(pattern="بوتي$"))
async def _(event):
    if event.fwd_from:
        return
    TG_BOT_USERNAME = Config.TG_BOT_USERNAME
    await event.reply(f"**- البوت الخاص بك هو** \n {TG_BOT_USERNAME}")



