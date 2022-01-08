import os

from userbot import jmthon
from userbot.utils import admin_cmd, sudo_cmd


@jmthon.on(admin_cmd(pattern=r"قراءة", outgoing=True))
@jmthon.on(sudo_cmd(pattern=r"قراءة", allow_sudo=True))
async def _(event):
    r = await event.client.download_media(await event.get_reply_message())
    a = open(r, "r")
    z = a.read()
    a.close()
    n = await event.reply("**يتـم قـراءة المـلف انتـظر**")
    if len(z) > 4095:
        await n.edit("** عذرا الحروف الموجوده في هذا الملف كبيرة جدا**")
    else:
        await event.client.send_message(event.chat_id, f"```{z}```")
        await n.delete()
    os.remove(b)

    """     المـلف لسـورس جمثـون حصرا اذا تاخذ الملـف اذكر رابط القنـاة رجاءا.!   """
