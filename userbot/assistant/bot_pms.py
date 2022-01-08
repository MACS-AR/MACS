# @MACS37 - < https://t.me/MACS37 >
# Copyright (C) 2021 - MACS-AR
# All rights reserved.
#
# This file is a part of < https://github.com/MACS-AR/MACS37 >
# Please read the GNU Affero General Public License in;
# < https://github.com/MACS-AR/JM-THON/blob/master/LICENSE
# ===============================================================
import re
from collections import defaultdict
from datetime import datetime
from typing import Optional, Union

from telethon import Button, events
from telethon.errors import UserIsBlockedError
from telethon.events import CallbackQuery, StopPropagation
from telethon.utils import get_display_name

from userbot import Config, jmthon

from ..core import check_owner, pool
from ..core.logger import logging
from ..core.session import tgbot
from ..helpers import reply_id
from ..helpers.utils import _format
from ..sql_helper.bot_blacklists import check_is_black_list
from ..sql_helper.bot_pms_sql import (
    add_user_to_db,
    get_user_id,
    get_user_logging,
    get_user_reply,
)
from ..sql_helper.bot_starters import add_starter_to_db, get_starter_details
from ..sql_helper.globals import delgvar, gvarstatus
from . import BOTLOG, BOTLOG_CHATID
from .botmanagers import ban_user_from_bot

LOGS = logging.getLogger(__name__)

plugin_category = "bot"
botusername = Config.TG_BOT_USERNAME


class FloodConfig:
    BANNED_USERS = set()
    USERS = defaultdict(list)
    MESSAGES = 3
    SECONDS = 6
    ALERT = defaultdict(dict)
    AUTOBAN = 10


async def check_bot_started_users(user, event):
    if user.id == Config.OWNER_ID:
        return
    check = get_starter_details(user.id)
    if check is None:
        start_date = str(datetime.now().strftime("%B %d, %Y"))
        notification = f"**▾∮ مرحبا عزيزي ↸**\n**▾ قام المستخدم ↫ ** 『{_format.mentionuser(user.first_name , user.id)}』 **بتشغيل البوت❕**\n**▾∮ الاسم ⪼** `{get_display_name(user)}`\n**▾∮الايدي ⪼ **`{user.id}`\n\n**⍣ⵧⵧⵧⵧⵧᴊᴍᴛʜᴏɴⵧⵧⵧⵧⵧ⍣**\n[𝙅𝙈𝙏𝙃𝙊𝙉 𝙐𝙎𝙀𝙍𝘽𝙊𝙏 🧸♥](https://t.me/MACS37)"
    else:
        start_date = check.date
        notification = f"**▾∮ قام المستخدم ↫ 「{_format.mentionuser(user.first_name , user.id)}」 بإعادة تشغيل البوت❗️**\n**▾∮الاسم ⪼ **`{get_display_name(user)}`\n**▾∮الايدي ⪼ ** `{user.id}`\n\n**⍣ⵧⵧⵧⵧⵧᴊᴍᴛʜᴏɴⵧⵧⵧⵧⵧ⍣**\n[𝙅𝙈𝙏𝙃𝙊𝙉 𝙐𝙎𝙀𝙍𝘽𝙊𝙏 🧸♥](https://t.me/MACS37)"

    try:
        add_starter_to_db(user.id, get_display_name(user), start_date, user.username)
    except Exception as e:
        LOGS.error(str(e))
    if BOTLOG:
        await event.client.send_message(BOTLOG_CHATID, notification)


@jmthon.bot_cmd(incoming=True, func=lambda e: e.is_private)
async def bot_pms(event):
    chat = await event.get_chat()
    if check_is_black_list(chat.id):
        return
    if chat.id != Config.OWNER_ID:
        msg = await event.forward_to(Config.OWNER_ID)
        try:
            add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
        except Exception as e:
            LOGS.error(str(e))
            if BOTLOG:
                await event.client.send_message(
                    BOTLOG_CHATID,
                    f"**خـطأ**\nأثناء تخزين تفاصيل الرسائل في قاعدة البيانات\n`{str(e)}`",
                )
    else:
        if event.text.startswith("/"):
            return
        reply_to = await reply_id(event)
        if reply_to is None:
            return
        users = get_user_id(reply_to)
        if users is None:
            return
        for usr in users:
            user_id = int(usr.chat_id)
            reply_msg = usr.reply_id
            user_name = usr.first_name
            break
        if user_id is not None:
            try:
                if event.media:
                    msg = await event.client.send_file(
                        user_id, event.media, caption=event.text, reply_to=reply_msg
                    )
                else:
                    msg = await event.client.send_message(
                        user_id, event.text, reply_to=reply_msg, link_preview=False
                    )
            except UserIsBlockedError:
                return await event.reply("هـذا البـوت تم حـظره بواسـطه المستخدم ")
            except Exception as e:
                return await event.reply(f"**خطـأ:**\n`{str(e)}`")
            try:
                add_user_to_db(
                    reply_to, user_name, user_id, reply_msg, event.id, msg.id
                )
            except Exception as e:
                LOGS.error(str(e))
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"**خـطأ**\nأثناء تخزين تفاصيل الرسائل في قاعدة البيانات\n`{str(e)}`",
                    )


@jmthon.bot_cmd(edited=True)
async def bot_pms_edit(event):  # sourcery no-metrics
    chat = await event.get_chat()
    if check_is_black_list(chat.id):
        return
    if chat.id != Config.OWNER_ID:
        users = get_user_reply(event.id)
        if users is None:
            return
        reply_msg = None
        for user in users:
            if user.chat_id == str(chat.id):
                reply_msg = user.message_id
                break
        if reply_msg:
            await event.client.send_message(
                Config.OWNER_ID,
                f"▾∮ قام المستخدم ↫  「{_format.mentionuser(get_display_name(chat) , chat.id)}」 بتعديل الرسالة⇅",
                reply_to=reply_msg,
            )
            msg = await event.forward_to(Config.OWNER_ID)
            try:
                add_user_to_db(msg.id, get_display_name(chat), chat.id, event.id, 0, 0)
            except Exception as e:
                LOGS.error(str(e))
                if BOTLOG:
                    await event.client.send_message(
                        BOTLOG_CHATID,
                        f"**خـطأ**\nأثناء تخزين تفاصيل الرسائل في قاعدة البيانات\n`{str(e)}`",
                    )
    else:
        reply_to = await reply_id(event)
        if reply_to is not None:
            users = get_user_id(reply_to)
            result_id = 0
            if users is None:
                return
            for usr in users:
                if event.id == usr.logger_id:
                    user_id = int(usr.chat_id)
                    reply_msg = usr.reply_id
                    result_id = usr.result_id
                    break
            if result_id != 0:
                try:
                    await event.client.edit_message(
                        user_id, result_id, event.text, file=event.media
                    )
                except Exception as e:
                    LOGS.error(str(e))


@tgbot.on(events.MessageDeleted)
async def handler(event):
    for msg_id in event.deleted_ids:
        users_1 = get_user_reply(msg_id)
        users_2 = get_user_logging(msg_id)
        if users_2 is not None:
            result_id = 0
            for usr in users_2:
                if msg_id == usr.logger_id:
                    user_id = int(usr.chat_id)
                    result_id = usr.result_id
                    break
            if result_id != 0:
                try:
                    await event.client.delete_messages(user_id, result_id)
                except Exception as e:
                    LOGS.error(str(e))
        if users_1 is not None:
            reply_msg = None
            for user in users_1:
                if user.chat_id != Config.OWNER_ID:
                    reply_msg = user.message_id
                    break
            try:
                if reply_msg:
                    users = get_user_id(reply_msg)
                    for usr in users:
                        user_id = int(usr.chat_id)
                        user_name = usr.first_name
                        break
                    if check_is_black_list(user_id):
                        return
                    await event.client.send_message(
                        Config.OWNER_ID,
                        f"▾∮ قام المستخدم ↫  「{_format.mentionuser(user_name , user_id)}」 بحذف الرسالة ↧",
                        reply_to=reply_msg,
                    )
            except Exception as e:
                LOGS.error(str(e))


@jmthon.bot_cmd(
    pattern=f"^معلومات$",
    from_users=Config.OWNER_ID,
)
async def bot_start(event):
    reply_to = await reply_id(event)
    if not reply_to:
        return await event.reply("**▾∮قم بالرد ع رسالة المستخدم لجلب المعلومات!**")
    info_msg = await event.client.send_message(
        event.chat_id,
        "**▾∮ سأجلب المعلومات من قاعدة بياناتي ✓",
        reply_to=reply_to,
    )
    users = get_user_id(reply_to)
    if users is None:
        return await info_msg.edit("حدث خطأ!\n**لم اعثر على المستخدم في بياناتي ✘**")
    for usr in users:
        user_id = int(usr.chat_id)
        user_name = usr.first_name
        break
    if user_id is None:
        return await info_msg.edit("حدث خطأ!\n**لم اعثر على المستخدم في بياناتي ✘**")
    uinfo = f"**▾∮الاسم ⪼ **`{user_name}`\n**▾∮الايدي ⪼ **`{user_id}`\n**▾∮الرابط ⪼** 「{_format.mentionuser(user_name , user_id)}」\n\n**⍣ⵧⵧⵧⵧⵧᴊᴍᴛʜᴏɴⵧⵧⵧⵧⵧ⍣**\n[𝙅𝙈𝙏𝙃𝙊𝙉 𝙐𝙎𝙀𝙍𝘽𝙊𝙏 🧸♥](https://t.me/MACS37)"
    await info_msg.edit(uinfo)


async def send_flood_alert(user_) -> None:
    # sourcery no-metrics
    buttons = [
        (
            Button.inline("حظر المستخدم ⛔️❗️", data=f"bot_pm_ban_{user_.id}"),
            Button.inline(
                "ايقاف تحذير التكرار ﹥[off] ⚠️",
                data="toggle_bot-antiflood_off",
            ),
        )
    ]
    found = False
    if FloodConfig.ALERT and (user_.id in FloodConfig.ALERT.keys()):
        found = True
        try:
            FloodConfig.ALERT[user_.id]["count"] += 1
        except KeyError:
            found = False
            FloodConfig.ALERT[user_.id]["count"] = 1
        except Exception as e:
            if BOTLOG:
                await jmthon.tgbot.send_message(
                    BOTLOG_CHATID, f"**Error:**\nWhile updating flood count\n`{str(e)}`"
                )
        flood_count = FloodConfig.ALERT[user_.id]["count"]
    else:
        flood_count = FloodConfig.ALERT[user_.id]["count"] = 1

    flood_msg = (
        r"تحذير التكرار ⚠️"
        "\n\n"
        f"**▾∮  المستخدم ⪼** 「{_format.mentionuser(get_display_name(user_), user_.id)}」\n**▾∮الايدي ⪼ **`{user_.id}`\n\n**▾ المستخدم قام بتكرار الرسائل! العدد ↫** `({flood_count})`\n`*عند الاهمال سيتم حظره تلقائي ❗️`\n**للاجراء السريع في الاسفل ↶** \n**⍣ⵧⵧⵧⵧⵧᴊᴍᴛʜᴏɴⵧⵧⵧⵧⵧ⍣**\n[𝙅𝙈𝙏𝙃𝙊𝙉 𝙐𝙎𝙀𝙍𝘽𝙊𝙏 🧸♥](https://t.me/MACS37)"
    )

    if found:
        if flood_count >= FloodConfig.AUTOBAN:
            if user_.id in Config.SUDO_USERS:
                sudo_spam = (
                    f"**Sudo User** {_format.mentionuser(user_.first_name , user_.id)}:\n  ID: {user_.id}\n\n"
                    "Is Flooding your bot !, Check `.help delsudo` to remove the user from Sudo."
                )
                if BOTLOG:
                    await jmthon.tgbot.send_message(BOTLOG_CHATID, sudo_spam)
            else:
                await ban_user_from_bot(
                    user_,
                    f"▾∮ حظر تلقائي لتكرارك {FloodConfig.AUTOBAN} رسائل!",
                )
                FloodConfig.USERS[user_.id].clear()
                FloodConfig.ALERT[user_.id].clear()
                FloodConfig.BANNED_USERS.remove(user_.id)
            return
        fa_id = FloodConfig.ALERT[user_.id].get("fa_id")
        if not fa_id:
            return
        try:
            msg_ = await jmthon.tgbot.get_messages(BOTLOG_CHATID, fa_id)
            if msg_.text != flood_msg:
                await msg_.edit(flood_msg, buttons=buttons)
        except Exception as fa_id_err:
            LOGS.debug(fa_id_err)
            return
    else:
        if BOTLOG:
            fa_msg = await jmthon.tgbot.send_message(
                BOTLOG_CHATID,
                flood_msg,
                buttons=buttons,
            )
        try:
            chat = await jmthon.tgbot.get_entity(BOTLOG_CHATID)
            await jmthon.tgbot.send_message(
                Config.OWNER_ID,
                f"⚠️  **[▾∮ يوجد تكرار!\nإضغط ع الرسالة لمعرفتهُ واجراء اللازم!](https://t.me/c/{chat.id}/{fa_msg.id})**",
            )
        except UserIsBlockedError:
            if BOTLOG:
                await jmthon.tgbot.send_message(BOTLOG_CHATID, "**Unblock your bot !**")
    if FloodConfig.ALERT[user_.id].get("fa_id") is None and fa_msg:
        FloodConfig.ALERT[user_.id]["fa_id"] = fa_msg.id


@jmthon.tgbot.on(CallbackQuery(data=re.compile(b"bot_pm_ban_([0-9]+)")))
@check_owner
async def bot_pm_ban_cb(c_q: CallbackQuery):
    user_id = int(c_q.pattern_match.group(1))
    try:
        user = await jmthon.get_entity(user_id)
    except Exception as e:
        await c_q.answer(f"Error:\n{str(e)}")
    else:
        await c_q.answer(f"جاري حظر المستخدم ↫ `{user_id}`", alert=False)
        await ban_user_from_bot(user, "لا يسمح بتكرار الرسائل!")
        await c_q.edit(
            f"▾∮ تم حظر المستخدم بسبب التكرار❗️ ↶**\n**▾∮الاسم ⪼ **`{user_name}`\n**▾∮الايدي ⪼ **`{user_id}`\n**▾∮الرابط ⪼** 「{_format.mentionuser(user_name , user_id)}**⍣ⵧⵧⵧⵧⵧᴊᴍᴛʜᴏɴⵧⵧⵧⵧⵧ⍣**\n[𝙅𝙈𝙏𝙃𝙊𝙉 𝙐𝙎𝙀𝙍𝘽𝙊𝙏 🧸♥](https://t.me/MACS37)"
        )


def time_now() -> Union[float, int]:
    return datetime.timestamp(datetime.now())


@pool.run_in_thread
def is_flood(uid: int) -> Optional[bool]:
    """Checks if a user is flooding"""
    FloodConfig.USERS[uid].append(time_now())
    if (
        len(
            list(
                filter(
                    lambda x: time_now() - int(x) < FloodConfig.SECONDS,
                    FloodConfig.USERS[uid],
                )
            )
        )
        > FloodConfig.MESSAGES
    ):
        FloodConfig.USERS[uid] = list(
            filter(
                lambda x: time_now() - int(x) < FloodConfig.SECONDS,
                FloodConfig.USERS[uid],
            )
        )
        return True


@jmthon.tgbot.on(CallbackQuery(data=re.compile(b"toggle_bot-antiflood_off$")))
@check_owner
async def settings_toggle(c_q: CallbackQuery):
    if gvarstatus("bot_antif") is None:
        return await c_q.answer(f" تحذير التكرار فعلا غير مفعل ❓", alert=False)
    delgvar("bot_antif")
    await c_q.answer(f" تم ايقاف تحذير التكرار ❗️", alert=False)
    await c_q.edit("**▾∮ تحذير التكرار غير مفعل الان  ✅**")


@jmthon.bot_cmd(incoming=True, func=lambda e: e.is_private)
@jmthon.bot_cmd(edited=True, func=lambda e: e.is_private)
async def antif_on_msg(event):
    if gvarstatus("bot_antif") is None:
        return
    chat = await event.get_chat()
    if chat.id == Config.OWNER_ID:
        return
    user_id = chat.id
    if check_is_black_list(user_id):
        raise StopPropagation
    elif await is_flood(user_id):
        await send_flood_alert(chat)
        FloodConfig.BANNED_USERS.add(user_id)
        raise StopPropagation
    elif user_id in FloodConfig.BANNED_USERS:
        FloodConfig.BANNED_USERS.remove(user_id)
