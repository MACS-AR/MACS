from userbot import jmthon
from userbot.core.logger import logging

from ..Config import Config
from ..helpers.utils import _format
from ..sql_helper import no_log_pms_sql
from ..sql_helper.globals import addgvar, gvarstatus

LOGS = logging.getLogger(__name__)

plugin_category = "utils"


class LOG_CHATS:
    def __init__(self):
        self.RECENT_USER = None
        self.NEWPM = None
        self.COUNT = 0


LOG_CHATS_ = LOG_CHATS()


@jmthon.ar_cmd(incoming=True, func=lambda e: e.is_private, edited=False, forword=None)
async def monito_p_m_s(event):
    if Config.PM_LOGGER_GROUP_ID == -100:
        return
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        return
    sender = await event.get_sender()
    if not sender.bot:
        chat = await event.get_chat()
        if not no_log_pms_sql.is_approved(chat.id) and chat.id != 777000:
            if LOG_CHATS_.RECENT_USER != chat.id:
                LOG_CHATS_.RECENT_USER = chat.id
                if LOG_CHATS_.NEWPM:
                    if LOG_CHATS_.COUNT > 1:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "- رسـالة جـديدة", f"{LOG_CHATS_.COUNT} "
                            )
                        )
                    else:
                        await LOG_CHATS_.NEWPM.edit(
                            LOG_CHATS_.NEWPM.text.replace(
                                "-  رسـالة جـديدة", f"{LOG_CHATS_.COUNT} "
                            )
                        )
                    LOG_CHATS_.COUNT = 0
                LOG_CHATS_.NEWPM = await event.client.send_message(
                    Config.PM_LOGGER_GROUP_ID,
                    f"- المستخدم {_format.mentionuser(sender.first_name , sender.id)}\n **⪼  قام بأرسال رسالة جديدة** \n▾∮ ايدي المستخدم: `{chat.id}`",
                )
            try:
                if event.message:
                    await event.client.forward_messages(
                        Config.PM_LOGGER_GROUP_ID, event.message, silent=True
                    )
                LOG_CHATS_.COUNT += 1
            except Exception as e:
                LOGS.warn(str(e))


@jmthon.ar_cmd(incoming=True, func=lambda e: e.mentioned, edited=False, forword=None)
async def log_tagged_messages(event):
    hmm = await event.get_chat()
    from .afk import AFK_

    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        return
    if (
        (no_log_pms_sql.is_approved(hmm.id))
        or (Config.PM_LOGGER_GROUP_ID == -100)
        or ("on" in AFK_.USERAFK_ON)
        or (await event.get_sender() and (await event.get_sender()).bot)
    ):
        return
    full = None
    try:
        full = await event.client.get_entity(event.message.from_id)
    except Exception as e:
        LOGS.info(str(e))
    messaget = media_type(event)
    resalt = f"- المجموعه : </b><code>{hmm.title}</code>"
    if full is not None:
        resalt += (
            f"\n<b> المرسل : </b> 👤{_format.htmlmentionuser(full.first_name , full.id)}"
        )
    if messaget is not None:
        resalt += f"\n<b> رسـالة جـديدة : </b><code>{messaget}</code>"
    else:
        resalt += f"\n<b>- رسـالة جـديدة: </b>{event.message.message}"
    resalt += f"\n<b>- رابط الرساله : </b><a href = 'https://t.me/c/{hmm.id}/{event.message.id}'> اضغط هنا</a>"
    if not event.is_private:
        await event.client.send_message(
            Config.PM_LOGGER_GROUP_ID,
            resalt,
            parse_mode="html",
            link_preview=False,
        )


@jmthon.on(admin_cmd(pattern="تخزين الخاص (تشغيل|ايقاف)$"))
async def set_pmlog(event):
    "لتشغـيل او ايقـاف تخـزين رسائل الـخاص"
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        h_type = False
    elif input_str == "تشغيل":
        h_type = True
    if gvarstatus("PMLOG") and gvarstatus("PMLOG") == "false":
        PMLOG = False
    else:
        PMLOG = True
    if PMLOG:
        if h_type:
            await event.edit("**⌯︙ تـخزين رسـائل الخـاص بالفـعل مُمكـنة ✅**")
        else:
            addgvar("PMLOG", h_type)
            await event.edit("**⌯︙ تـم تعـطيل تخـزين رسائل الـخاص بنـجاح ✅**")
    elif h_type:
        addgvar("PMLOG", h_type)
        await event.edit("**⌯︙ تـم تفعيل تخـزين رسائل الـخاص بنـجاح ✅**")
    else:
        await event.edit("**⌯︙ تـخزين رسـائل الخـاص بالفـعل معـطلة ✅**")


@jmthon.on(admin_cmd(pattern="تخزين الكروبات (تشغيل|ايقاف)$"))
async def set_grplog(event):
    "لتشغـيل او ايقـاف تخـزين رسائل الكروبات"
    input_str = event.pattern_match.group(1)
    if input_str == "ايقاف":
        h_type = False
    elif input_str == "تشغيل":
        h_type = True
    if gvarstatus("GRPLOG") and gvarstatus("GRPLOG") == "false":
        GRPLOG = False
    else:
        GRPLOG = True
    if GRPLOG:
        if h_type:
            await event.edit("**⌯︙ تـخزين رسـائل الكروبات بالفـعل مُمكـنة ✅**")
        else:
            addgvar("GRPLOG", h_type)
            await event.edit("**⌯︙ تـم تعـطيل تخـزين رسائل الكروبات بنـجاح ✅**")
    elif h_type:
        addgvar("GRPLOG", h_type)
        await event.edit("**⌯︙ تـم تفعيل تخـزين رسائل الكروبات بنـجاح ✅**")
    else:
        await event.edit("**⌯︙ تـخزين رسـائل الكروبات بالفـعل معـطلة ✅**")
