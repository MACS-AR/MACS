from asyncio import sleep

from telethon.errors import ChatAdminRequiredError, UserAdminInvalidError
from telethon.tl import functions
from telethon.tl.functions.channels import EditBannedRequest
from telethon.tl.types import (
    ChannelParticipantsAdmins,
    ChatBannedRights,
    UserStatusEmpty,
    UserStatusLastMonth,
    UserStatusLastWeek,
    UserStatusOffline,
    UserStatusOnline,
    UserStatusRecently,
)
#
from userbot import jmthon
from telethon.tl.types import ChannelParticipantsKicked

from userbot import jmthon, CMD_HELP

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from . import BOTLOG, BOTLOG_CHATID

LOGS = logging.getLogger(__name__)

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,
)


async def ban_user(chat_id, i, rights):
    try:
        await jmthon(functions.channels.EditBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)





@jmthon.on(admin_cmd(pattern="حذف المحظورين(?: |$)(.*)"))
async def _(event):
    await event.edit("**- يتم التعـرف انتـظر قليـلا من فضلك**")
    p = 0
    (await event.get_chat()).title
    async for i in event.client.iter_participants(
        event.chat_id,
        filter=ChannelParticipantsKicked,
        aggressive=True,
    ):
        try:
            await event.client.edit_permissions(event.chat_id, i, view_messages=True)
            p += 1
        except BaseException:
            pass
    await event.edit("**- تم حذف جميع المحظورين بنجاح ✓**")


@bot.on(admin_cmd(pattern=r"تفليش$"))
async def _(event):
    result = await event.client.get_permissions(event.chat_id, event.client.uid)
    if not result:
        return await edit_or_reply(
            event, "عذر ليس لديك الصلاحيات الكافية لاستخدام هذا الامر"
        )
    jmthonevent = await edit_or_reply(event, "جـارِ")
    admins = await event.client.get_participants(
        event.chat_id, filter=ChannelParticipantsAdmins
    )
    admins_id = [i.id for i in admins]
    total = 0
    success = 0
    async for user in event.client.iter_participants(event.chat_id):
        total += 1
        try:
            if user.id not in admins_id:
                await event.client(
                    EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS)
                )
                success += 1
                await sleep(0.5)
        except Exception as e:
            LOGS.info(str(e))
            await sleep(0.5)
    await jmthonevent.edit(
        f"- تم بنجاح التفليش  {success} من {total} الاعضاء"
    )


@jmthon.on(admin_cmd(pattern="المحذوفين ?([\s\S]*)"))
async def rm_deletedacc(show):
    con = show.pattern_match.group(1).lower()
    del_u = 0
    del_status = " لم يتم العثور على حسابات متروكه او حسابات محذوفة الكروب نظيف"
    if con != "اطردهم":
        event = await edit_or_reply(
            show, " يتم البحث عن حسابات محذوفة او حسابات متروكة انتظر"
        )
        async for user in show.client.iter_participants(show.chat_id):
            if user.deleted:
                del_u += 1
                await sleep(0.5)
        if del_u > 0:
            del_status = f"تـم العـثور : **{del_u}** على حسابات محذوفة ومتروكه في هذه الدردشه من الحسابات في هذه الدردشه,\
                           \nاطردهم بواسطه  `.المحذوفين اطردهم`"
        await event.edit(del_status)
        return
    chat = await show.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_delete(show, "أنا لسـت مشرف هـنا", 5)
        return
    event = await edit_or_reply(show, "جاري حذف الحسابات المحذوفة")
    del_u = 0
    del_a = 0
    async for user in show.client.iter_participants(show.chat_id):
        if user.deleted:
            try:
                await show.client.kick_participant(show.chat_id, user.id)
                await sleep(0.5)
                del_u += 1
            except ChatAdminRequiredError:
                await edit_delete(event, " ليس لدي صلاحيات الحظر هنا", 5)
                return
            except UserAdminInvalidError:
                del_a += 1
    if del_u > 0:
        del_status = f"التنظيف **{del_u}** من الحسابات المحذوفة"
    if del_a > 0:
        del_status = f"التنظيف **{del_u}** من الحسابات المحذوف \
        \n**{del_a}** لا يمكنني حذف حسابات المشرفين المحذوفة"
    await edit_delete(event, del_status, 5)
    if BOTLOG:
        await show.client.send_message(
            BOTLOG_CHATID,
            f"#تنـظيف الـمحذوفات\
            \n{del_status}\
            \nالـدردشة: {show.chat.title}(`{show.chat_id}`)",
        )


@jmthon.on(admin_cmd(pattern="احصائيات الاعضاء ?([\s\S]*)"))
async def _(event):
    input_str = event.pattern_match.group(1)
    if input_str:
        chat = await event.get_chat()
        if not chat.admin_rights and not chat.creator:
            await edit_or_reply(event, " انت لست مشرف هنا ⌔︙")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    e = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    et = await edit_or_reply(event, "يتم البحث في القوائم ⌔︙")
    async for i in event.client.iter_participants(event.chat_id):
        p += 1
        #
        # Note that it's "reversed". You must set to ``True`` the permissions
        # you want to REMOVE, and leave as ``None`` those you want to KEEP.
        rights = ChatBannedRights(until_date=None, view_messages=True)
        if isinstance(i.status, UserStatusEmpty):
            y += 1
            if "y" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit(" احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastMonth):
            m += 1
            if "m" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit(" احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusLastWeek):
            w += 1
            if "w" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit(" احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
        if isinstance(i.status, UserStatusOffline):
            o += 1
            if "o" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit(" احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusOnline):
            q += 1
            if "q" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit(" احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
                else:
                    c += 1
        if isinstance(i.status, UserStatusRecently):
            r += 1
            if "r" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
        if i.bot:
            b += 1
            if "b" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if not status:
                    await et.edit("احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
                    break
                else:
                    c += 1
        elif i.deleted:
            d += 1
            if "d" in input_str:
                status, e = await ban_user(event.chat_id, i, rights)
                if status:
                    c += 1
                else:
                    await et.edit("احتاج الى صلاحيات المشرفين للقيام بهذا الامر ")
                    e.append(str(e))
        elif i.status is None:
            n += 1
    if input_str:
        required_string = """الـمطرودين {} / {} الأعـضاء
الحـسابـات المـحذوفة: {}
حـالة المستـخدم الفـارغه: {}
اخر ظهور منذ شـهر: {}
اخر ظـهور منـذ اسبوع: {}
غير متصل: {}
المستخدمين النشطون: {}
اخر ظهور قبل قليل: {}
البوتات: {}
مـلاحظة: {}"""
        await et.edit(required_string.format(c, p, d, y, m, w, o, q, r, b, n))
        await sleep(5)
    await et.edit(
        """: {} مـجموع المـستخدمين
الحـسابـات المـحذوفة: {}
حـالة المستـخدم الفـارغه: {}
اخر ظهور منذ شـهر: {}
اخر ظـهور منـذ اسبوع: {}
غير متصل: {}
المستخدمين النشطون: {}
اخر ظهور قبل قليل: {}
البوتات: {}
مـلاحظة: {}""".format(
            p, d, y, m, w, o, q, r, b, n
        )
    )


CMD_HELP.update(
    {
        "اوامر الكروب": "•  .حذف المحظورين\n فقط اكتب الامر لحذف جميع المحظورين في المجموعه\
         \n\n• .المحذوفين\n   اكتب الامر لعرض الحسابات المحذوفه في المجموعة وحذفها\
         \n\n• .احصائيات الاعضاء\n      لعرض احصائيات الاعضاء في المجموعه يجب ان تكون مشرف\
         \n\n• .تفليش\n    فقط اكتب الامر لتفليذ المجموعه يجب ان تكون مشرف"
    }
)
