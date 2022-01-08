from telethon.tl.types import Channel, MessageMediaWebPage
from userbot.utils import admin_cmd
from userbot import CMD_HELP


class FPOST:
    def __init__(self) -> None:
        self.GROUPSID = []
        self.MSG_CACHE = {}


FPOST_ = FPOST()


async def all_groups_id(roz):
    rozgroups = []
    async for dialog in roz.client.iter_dialogger():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.megagroup:
            rozgroups.append(entity.id)
    return rozgroups


@jmthon.on(admin_cmd(pattern="ارسل$"))
async def _(event):
    try:
        await event.delete()
    except Exception as e:
        logger.info(str(e))
    m = await event.get_reply_message()
    if not m:
        return
    if m.media and not isinstance(m.media, MessageMediaWebPage):
        return await event.client.send_file(event.chat_id, m.media, caption=m.text)
    await event.client.send_message(event.chat_id, m.text)

CMD_HELP.update(
    {
        "الارسال": "\n.ارسل <بالرد ؏ ايشي>\nيستخدم حتى يعيد ارسال النص او ملف او ايشي شخص رسله فقط رد عليه بالامر "
    }
)
