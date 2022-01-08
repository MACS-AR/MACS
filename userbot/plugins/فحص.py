import random
import time
from datetime import datetime
from platform import python_version
from telethon import version
from telethon.errors.rpcerrorlist import (
    MediaEmptyError,
    WebpageCurlFailedError,
    WebpageMediaEmptyError,
)

from userbot import JMVERSION, StartTime, jmthon
from ..core.managers import edit_or_reply
from ..helpers.functions import check_data_base_heal_th, get_readable_time
from ..helpers.utils import reply_id
from ..sql_helper.globals import gvarstatus
from . import *




@jmthon.on(admin_cmd(pattern="فحص(?: |$)(.*)"))
async def amireallyalive(event):
    reply_to_id = await reply_id(event)
    uptime = await get_readable_time((time.time() - StartTime))
    start = datetime.now()
    await edit_or_reply(event, "** ⌯︙يتـم التـأكـد انتـظر قليلا رجاءا**")
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    _, check_sgnirts = check_data_base_heal_th()
    EMOJI = gvarstatus("ALIVE_EMOJI") or "  - "
    ALIVE_TEXT = gvarstatus("ALIVE_TEXT") or "** بـوت ماكس يعـمل بنـجـاح **"
    RR7_IMG = gvarstatus("ALIVE_PIC")
    jmthon_caption = gvarstatus("ALIVE_TEMPLATE") or temp
    caption = jmthon_caption.format(
        ALIVE_TEXT=ALIVE_TEXT,
        EMOJI=EMOJI,
        mention=mention,
        uptime=uptime,
        telever=version.__version__,
        jmver=JMVERSION,
        pyver=python_version(),
        dbhealth=check_sgnirts,
        ping=ms,
    )
    if RR7_IMG:
        RR7 = [x for x in RR7_IMG.split()]
        PIC = random.choice(RR7)
        try:
            await event.client.send_file(
                event.chat_id, PIC, caption=caption, reply_to=reply_to_id
            )
            await event.delete()
        except (WebpageMediaEmptyError, MediaEmptyError, WebpageCurlFailedError):
            return await edit_or_reply(
                event,
                f"**الميـديا خـطأ **\nغـير الرابـط بأستـخدام الأمـر  \n `.اضف_فار ALIVE_PIC رابط صورتك`\n\n**لا يمـكن الحـصول عـلى صـورة من الـرابـط :-** `{PIC}`",
            )
    else:
        await edit_or_reply(
            event,
            caption,
        )


temp = """- {ALIVE_TEXT}

**{EMOJI} قاعدۿ البيانات :** تعمل بنـجاح
**{EMOJI} أصـدار التـيليثون :** `{telever}`
**{EMOJI} أصـدار ماكس :** `{jmver}`
**{EMOJI} الوقت:** `{uptime}` 
**{EMOJI} أصدار البـايثون :** `{pyver}`
**{EMOJI} المسـتخدم:** {mention}"""


@jmthon.on(admin_cmd(pattern="امر فحص(?: |$)(.*)"))
async def _(event):
    if not event.text[0].isalpha() and event.text[0] not in ("/", "#", "@", "!"):
        await event.edit(ALIVERZ)
