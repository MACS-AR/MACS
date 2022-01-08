from telethon.tl.types import Channel, MessageMediaWebPage

from userbot import jmthon
from userbot.core.logger import logging

plugin_category = "extra"

LOGS = logging.getLogger(__name__)


class FPOST:
    def __init__(self) -> None:
        self.GROUPSID = []
        self.MSG_CACHE = {}


FPOST_ = FPOST()


async def all_groups_id(roz):
    rozgroups = []
    async for dialog in roz.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.megagroup:
            rozgroups.append(entity.id)
    return rozgroups


@jmthon.ar_cmd(
    pattern="ارسل$",
    command=("ارسل", plugin_category),
)
async def _(event):
    "To resend the message again"
    try:
        await event.delete()
    except Exception as e:
        LOGS.info(str(e))
    m = await event.get_reply_message()
    if not m:
        return
    if m.media and not isinstance(m.media, MessageMediaWebPage):
        return await event.client.send_file(event.chat_id, m.media, caption=m.text)
    await event.client.send_message(event.chat_id, m.text)
