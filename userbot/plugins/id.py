from telethon.utils import pack_bot_file_id

from userbot import jmthon
from userbot.core.logger import logging

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"

LOGS = logging.getLogger(__name__)


@jmthon.ar_cmd(
    pattern="(الايدي|id)(?:\s|$)([\s\S]*)",
    command=("الايدي", plugin_category),
    info={
        "header": "للحـصـول عـلى ايـدي المجـموعة او المستـخدم.",
        "description": "بالـرد عـلى شخـص للحصـول عـلى ايديه او بـوضع معرفه مع الامـر واذا لم تقـم بوضع معرفه او بالـرد عليه سيعطيك ايـدي الدردشة الحالية",
        "usage": "{tr}الايدي <باارد/معرف>",
    },
)
async def _(event):
    "للحـصـول عـلى ايـدي المجـموعة او المستـخدم.."
    input_str = event.pattern_match.group(2)
    if input_str:
        try:
            p = await event.client.get_entity(input_str)
        except Exception as e:
            return await edit_delete(event, f"`{str(e)}`", 5)
        try:
            if p.first_name:
                return await edit_or_reply(
                    event, f"⌯︙ايدي المستخدم : `{input_str}` هو `{p.id}`"
                )
        except Exception:
            try:
                if p.title:
                    return await edit_or_reply(
                        event, f"⌯︙ايدي الدردشة/القناة `{p.title}` هو `{p.id}`"
                    )
            except Exception as e:
                LOGS.info(str(e))
        await edit_or_reply(event, "⌯︙يـجب كـتابة مـعرف الشـخص او الـرد عـليه")
    elif event.reply_to_msg_id:
        await event.get_input_chat()
        r_msg = await event.get_reply_message()
        if r_msg.media:
            bot_api_file_id = pack_bot_file_id(r_msg.media)
            await edit_or_reply(
                event,
                f"⌯︙ايدي الدردشه: `{str(event.chat_id)}` \n⌯︙ايدي المستخدم: `{str(r_msg.sender_id)}` \n⌯︙ايدي الميديا: `{bot_api_file_id}`",
            )
        else:
            await edit_or_reply(
                event,
                f"⌯︙ايدي الدردشه : `{str(event.chat_id)}` \n⌯︙ايدي المستخدم: `{str(r_msg.sender_id)}` ",
            )
    else:
        await edit_or_reply(event, f"⌯︙الـدردشـة الـحالية : `{str(event.chat_id)}`")
