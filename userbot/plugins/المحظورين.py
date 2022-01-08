import asyncio
from time import sleep
#
from telethon.tl import functions
from telethon.tl.types import (
    ChannelParticipantsKicked,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)
from userbot.utils import admin_cmd
from userbot import CMD_HELP, jmthon


@jmthon.on(admin_cmd(pattern="حذف المحظورين ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    input_r = event.pattern_match.group(1)
    if input_r:
        logger.info("**لم ينفذ هذا الامر**")
    else:
        if event.is_private:
            return False
        await event.edit("**- يتم التعرف انتظر قليلا  .**")
        p = 0
        async for i in borg.iter_participants(
            event.chat_id, filter=ChannelParticipantsKicked, aggressive=True
        ):
            jmthon = ChatBannedRights(until_date=0, view_messages=False)
            try:
                await borg(
                    functions.channels.EditBannedRequest(event.chat_id, i, jmthon)
                )
            except FloodWaitError as ex:
                logger.warn("تم ايقاف لـ {} من الثواني".format(ex.seconds))
                sleep(ex.seconds)
            except Exception as ex:
                await event.edit(str(ex))
            else:
                p += 1
        await event.edit("{}: {} تم الغاء الحظر بنجاح  ✓".format(event.chat_id, p))


CMD_HELP.update(
    {
      "المحظورين": "**المحظورين**\
\n\n**الامر : **`.حذف المحظورين`\
\n**الاستخدام :** لألغاء حظر جميع المستخدمين في الدردشة"
})
