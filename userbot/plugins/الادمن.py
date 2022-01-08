"""
Userbot module to help you manage a group
"""
import asyncio

# جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
from asyncio import sleep
from os import remove

from telethon.errors import (
    BadRequestError,
    ChatAdminRequiredError,
    ImageProcessFailedError,
    PhotoCropSizeSmallError,
)
from telethon.errors.rpcerrorlist import MessageTooLongError
from telethon.tl.functions.channels import (  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
    EditAdminRequest,
    EditBannedRequest,
    EditPhotoRequest,
)
from telethon.tl.functions.messages import UpdatePinnedMessageRequest
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import (  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
    ChannelParticipantsAdmins,
    ChatAdminRights,
    ChatBannedRights,
    MessageEntityMentionName,
    MessageMediaPhoto,
)

from userbot import BOTLOG, BOTLOG_CHATID, jmthon
from userbot.utils import admin_cmd, errors_handler

from ..core.logger import logging
from ..core.managers import edit_delete
from ..core.managers import edit_or_reply
from ..core.managers import edit_or_reply as eor
from ..helpers.utils import _format, get_user_from_event
from ..sql_helper.mute_sql import is_muted, mute, unmute
from . import BOTLOG, BOTLOG_CHATID, get_user_from_event

# =================== الثوابت ===================
PP_TOO_SMOL = "**الصورة صغيرة جدًا** "
PP_ERROR = "**فشل أثناء معالجة الصورة** "
NO_ADMIN = "**انا لست مشرف هنا!!** "
NO_PERM = "**ليس لدي أذونات كافية!** "
CHAT_PP_CHANGED = "**تم تغيير صورة الدردشة بنجاح ✅**"
INVALID_MEDIA = "**الملحق غير صالح** "

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
UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)
# ================================================
from telethon.errors import BadRequestError
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import ChatBannedRights

from userbot import jmthon

from ..core.logger import logging
from ..core.managers import edit_delete, edit_or_reply
from ..helpers import media_type
from ..helpers.utils import _format
from . import BOTLOG, BOTLOG_CHATID

# =================== STRINGS ============
PP_TOO_SMOL = "**الصورة صغيرة جدًا** "
PP_ERROR = "**فشل أثناء معالجة الصورة** "
NO_ADMIN = "**انا لست مشرف هنا!!** "
NO_PERM = "**ليس لدي أذونات كافية!** "
CHAT_PP_CHANGED = "**تم تغيير صورة الدردشة بنجاح ✅**"
INVALID_MEDIA = "**الملحق غير صالح** "

BANNED_RIGHTS = ChatBannedRights(
    until_date=None,
    view_messages=True,
    send_messages=True,
    send_media=True,
    send_stickers=True,
    send_gifs=True,
    send_games=True,
    send_inline=True,
    embed_links=True,  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
)

UNBAN_RIGHTS = ChatBannedRights(
    until_date=None,
    send_messages=None,  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
    send_media=None,
    send_stickers=None,
    send_gifs=None,
    send_games=None,
    send_inline=None,
    embed_links=None,
)  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #

LOGS = logging.getLogger(__name__)
MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)


@jmthon.on(admin_cmd(outgoing=True, pattern="ضع صورة"))
@errors_handler
async def set_group_photo(gpic):
    if not gpic.is_group:
        await gpic.eor(event, "** عذرا عليك استخدام الامر في المجموعات فقط**")
        return
    replymsg = await gpic.get_reply_message()
    chat = await gpic.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    photo = None
    if not admin and not creator:
        x = await gpic.eor(x, NO_ADMIN)
        return
    if replymsg and replymsg.media:
        if isinstance(replymsg.media, MessageMediaPhoto):
            photo = await gpic.client.download_media(message=replymsg.photo)
        elif "image" in replymsg.media.document.mime_type.split("/"):
            photo = await gpic.client.download_file(replymsg.media.document)
        else:
            x = await gpic.eor(x, INVALID_MEDIA)
    if photo:
        try:
            await gpic.client(
                EditPhotoRequest(gpic.chat_id, await gpic.client.upload_file(photo))
            )
            x = await gpic.eor(x, CHAT_PP_CHANGED)
        except PhotoCropSizeSmallError:
            x = await gpic.eor(x, PP_TOO_SMOL)
        except ImageProcessFailedError:
            x = await gpic.eor(x, PP_ERROR)


@jmthon.on(admin_cmd("رفع مشرف(?: |$)(.*)"))
@errors_handler
async def promote(promt):
    chat = await promt.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await edit_or_reply(promt, NO_ADMIN)
        return
    new_rights = ChatAdminRights(
        add_admins=False,
        invite_users=True,
        change_info=False,
        ban_users=True,
        delete_messages=True,
        pin_messages=True,
    )
    roz = await edit_or_reply(promt, "** • يتم الرفع انتظر لحضه  **")
    user, rank = await get_user_from_event(promt)
    if not rank:
        rank = "مشرف مميز"
    if not user:
        return
    try:
        await promt.client(EditAdminRequest(promt.chat_id, user.id, new_rights, rank))
        await roz.edit("**تم رفعه مشرف بالمجموعه بنجاح  ✓**")
    except BadRequestError:
        await roz.edit(NO_PERM)
        return
    if BOTLOG:
        await promt.client.send_message(
            BOTLOG_CHATID,
            f"•، الـرفـع\
            \nالـمستخـدم: [{user.first_name}](tg://user?id={user.id})\
            \nالـدردشـة: {event.chat.title} (`{event.chat_id}`)",
        )


@jmthon.on(admin_cmd(outgoing=True, pattern="تنزيل مشرف(?: |$)(.*)"))
@errors_handler
async def demote(dmodroz):
    chat = await dmodroz.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await dmodroz.edit(NO_ADMIN)
        return
    await dmodroz.edit("• يتم التنزيل انتظر لحضه ")
    rank = "Admeen"  # dummy rank, lol.
    user = await get_user_from_event(dmodroz)
    user = user[0]
    if user:
        pass
    else:
        return
    newrights = ChatAdminRights(
        add_admins=None,
        invite_users=None,
        change_info=None,
        ban_users=None,
        delete_messages=None,
        pin_messages=None,
    )
    try:
        await dmodroz.client(
            EditAdminRequest(dmodroz.chat_id, user.id, newrights, rank)
        )
    except BadRequestError:
        await eor(dmodroz, NO_PERM)
        return
    await eor(dmodroz, "**تـم تنزيله من قائمه الادمنيه بنجاح ✓**")
    if BOTLOG:
        await dmodroz.client.send_message(
            BOTLOG_CHATID,
            f"• انزال الرتبة\
            \nالمعرف: [{user.first_name}](tg://user?id={user.id})\
            \nالدردشه: {event.chat.title}(`{event.chat_id}`)",
        )


@jmthon.on(admin_cmd(outgoing=True, pattern="الادمنية$"))
@errors_handler
async def get_admin(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = f"<b>مشرفين المجموعة في {title}:</b> \n"
    try:  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
        async for user in show.client.iter_participants(
            show.chat_id, filter=ChannelParticipantsAdmins
        ):
            if not user.deleted:
                link = f'<a href="tg://user?id={user.id}">{user.first_name}</a>'
                userid = f"<code>{user.id}</code>"
                mentions += f"\n{link} {userid}"
            else:
                mentions += f"\nالحسابات المحذوفة <code>{user.id}</code>"
    except ChatAdminRequiredError as err:
        mentions += " " + str(err) + "\n"
    await show.edit(mentions, parse_mode="html")


@jmthon.on(admin_cmd(outgoing=True, pattern="تثبيت(?: |$)(.*)"))
@errors_handler
async def pin(msg):
    chat = await msg.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    if not admin and not creator:
        await eor(msg, NO_ADMIN)
        return
    to_pin = msg.reply_to_msg_id
    if not to_pin:
        await eor(msg, "• يجب الرد على الرسالة لتثبيتهـا")
        return
    options = msg.pattern_match.group(1)
    is_silent = True
    if options.lower() == "loud":
        is_silent = False
    try:
        await msg.client(UpdatePinnedMessageRequest(msg.to_id, to_pin, is_silent))
    except BadRequestError:
        await eor(msg, NO_PERM)
        return
    await eor(msg, "- تم التثبيت بنجاح ✓")
    user = await get_user_from_id(msg.sender_id, msg)
    if BOTLOG:
        await msg.client.send_message(
            BOTLOG_CHATID,
            "التثبيت \n"
            f"الادمن : [{user.first_name}](tg://user?id={user.id})\n"
            f"الدردشة : {msg.chat.title}(`{msg.chat_id}`)\n",
        )


@jmthon.on(admin_cmd(outgoing=True, pattern="طرد(?: |$)(.*)"))
@errors_handler
async def kick(usr):
    chat = await usr.get_chat()
    admin = chat.admin_rights
    creator = chat.creator
    # If not admin and not creator, return
    if not admin and not creator:
        await eor(usr, NO_ADMIN)
        return
    user, reason = await get_user_from_event(usr)
    if not user:
        await eor(usr, "**-  لم يتم التـعرف عـلى المستخـدم**")
        return
    await eor(usr, "• يتم طرد المستخدم انتظر")
    try:
        await usr.client.kick_participant(usr.chat_id, user.id)
        await sleep(0.5)
    except Exception as e:
        await eor(usr, NO_PERM + f"\n{str(e)}")
        return
    if reason:
        await eor(
            usr,
            f"- المستخدم  [{user.first_name}](tg://user?id={user.id})\n تـم طرده بنجاح ✓ \nالسبب : {reason}",
        )
    else:
        await eor(
            usr,
            "- المستخدم  [{user.first_name}](tg://user?id={user.id})\n تـم طرده بنجاح ✓",
        )


@jmthon.on(admin_cmd(outgoing=True, pattern="المستخدمين ?(.*)"))
@errors_handler
async def get_users(show):
    info = await show.client.get_entity(show.chat_id)
    title = info.title if info.title else "this chat"
    mentions = "• المستخـدميـن في  {}: \n".format(title)
    try:
        if not show.pattern_match.group(1):
            async for user in show.client.iter_participants(show.chat_id):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:
                    mentions += f"\n ~ الحسابات المحذوفة `{user.id}`"
        else:
            searchq = show.pattern_match.group(1)
            async for user in show.client.iter_participants(
                show.chat_id, search=f"{searchq}"
            ):
                if not user.deleted:
                    mentions += (
                        f"\n[{user.first_name}](tg://user?id={user.id}) `{user.id}`"
                    )
                else:  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
                    mentions += f"\n~ الحسابات المحذوفة `{user.id}`"
    except ChatAdminRequiredError as roz:
        mentions += " " + str(roz) + "\n"
    try:
        await eor(show, mentions)
    except MessageTooLongError:
        await eor(
            show, "** عذرا اعضاء هذه المجموعة كثيرين لذلك تم عمل ملف للمستخدمين**"
        )
        file = open("userslist.txt", "w+")
        file.write(mentions)
        file.close()
        await show.client.send_file(
            show.chat_id,
            "userslist.txt",
            caption="المستخدمين فـي {}".format(title),
            reply_to=show.id,
        )
        remove("userslist.txt")


async def get_user_from_event(event):
    args = event.pattern_match.group(1).split(" ", 1)
    extra = None
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        user_obj = await event.client.get_entity(previous_message.sender_id)
        extra = event.pattern_match.group(1)
    elif args:
        user = args[0]
        if len(args) == 2:
            extra = args[1]
        if user.isnumeric():
            user = int(user)
        if not user:
            await eor(event, "**- يجب وضع معرف المستخدم او ايديه او الرد عليه**")
            return
        if event.message.entities is not None:
            probable_user_mention_entity = event.message.entities[0]
            if isinstance(probable_user_mention_entity, MessageEntityMentionName):
                user_id = probable_user_mention_entity.user_id
                user_obj = await event.client.get_entity(user_id)
                return user_obj
        try:
            user_obj = await event.client.get_entity(user)
        except (TypeError, ValueError) as err:
            await eor(event, str(err))
            return None
    return user_obj, extra


async def get_user_from_id(user, event):
    if isinstance(user, str):
        user = int(user)
    try:
        user_obj = await event.client.get_entity(user)
    except (TypeError, ValueError) as err:
        await eor(event, str(err))
        return None
    return user_obj


@jmthon.on(admin_cmd(pattern="حظر(?:\s|$)([\s\S]*)"))
async def _ban_person(event):
    user, reason = await get_user_from_event(event)
    if not user:
        return
    rozevent = await edit_or_reply(event, "تـم حـظره بـنجاح")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, BANNED_RIGHTS))
    except BadRequestError:
        return await rozevent.edit(NO_PERM)
    try:
        reply = await event.get_reply_message()
        if reply:
            await reply.delete()
    except BadRequestError:
        return await rozevent.edit("ليـس لـدي جـميع الصـلاحيـات لكـن سيـبقى محـظور")
    if reason:
        await rozevent.edit(
            f"المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n تـم حـظره بنـجاح !!\n**⌔︙السبب : **`{reason}`"
        )
    else:
        await rozevent.edit(
            f"المسـتخدم {_format.mentionuser(user.first_name ,user.id)} \n تـم حـظره بنـجاح ✅"
        )
    if BOTLOG:
        if reason:  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
            await event.client.send_message(
                BOTLOG_CHATID,
                f"الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \nايدي الكروب(`{event.chat_id}`)\
                \nالسبـب : {reason}",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                f"الحـظر\
                \nالمسـتخدم: [{user.first_name}](tg://user?id={user.id})\
                \nالـدردشـة: {event.chat.title}\
                \n ايـدي الكـروب: (`{event.chat_id}`)",
            )


@jmthon.on(admin_cmd(pattern="الغاء حظر(?:\s|$)([\s\S]*)"))
async def nothanos(event):
    user, _ = await get_user_from_event(event)
    if not user:
        return
    rozevent = await edit_or_reply(event, "جـار الـغاء الـحظر أنتـظر رجـاءا")
    try:
        await event.client(EditBannedRequest(event.chat_id, user.id, UNBAN_RIGHTS))
        await rozevent.edit(
            f"الـمستخدم {_format.mentionuser(user.first_name ,user.id)}\n تـم الـغاء حـظره بنـجاح "
        )
        if BOTLOG:
            await event.client.send_message(
                BOTLOG_CHATID,
                "الـغاء الـحظر \n"
                f"الـمستخدم: [{user.first_name}](tg://user?id={user.id})\n"
                f"الـدردشـة: {event.chat.title}(`{event.chat_id}`)",
            )
    except UserIdInvalidError:
        await rozevent.edit("يـبدو أن هذه الـعمليـة تم إلغاؤهـا")
    except Exception as e:  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
        await rozevent.edit(f"**خـطأ :**\n`{e}`")


# =================== الكـــــــــــــــتم  ===================  #


@jmthon.on(admin_cmd(pattern="كتم(?:\s|$)([\s\S]*)"))
async def startgmute(event):  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
    if event.is_private:
        await event.edit("**... قـد تحـدث بعـض المـشاكـل أو الأخـطاء ...**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return
        if user.id == jmthon.uid:
            return await edit_or_reply(event, "**... . لمـاذا تࢪيـد كتم نفسـك؟  ...**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event, "**... غيـر قـادر عـلى جـلب مـعلومات الـشخص ..**"
        )
    if is_muted(userid, "gmute"):
        return await edit_or_reply(
            event,
            f"**... هـذا الشـخص مكـتوم بـنجاح ...**",
        )
    try:
        mute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خـطأ**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"** تـم كـتم الـمستخـدم بـنجاح  ،🔕 **",
            )
        else:
            await edit_or_reply(
                event,
                f"** تـم كـتم الـمستخـدم بـنجاح  ،🔕 **",
            )
    if BOTLOG:
        reply = await event.get_reply_message()
        if reason:  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
            await event.client.send_message(
                BOTLOG_CHATID,
                " الـكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**السبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                " الـكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )
        if reply:
            await reply.forward_to(BOTLOG_CHATID)


# =================== الغـــــــــــــاء الكـــــــــــــــتم  ===================  #

# جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
@jmthon.on(admin_cmd(pattern="الغاء كتم(?:\s|$)([\s\S]*)"))
async def endgmute(event):
    if event.is_private:
        await event.edit("**... قـد تحـدث بعـض المـشاكـل أو الأخـطاء ...**")
        await asyncio.sleep(2)
        userid = event.chat_id
        reason = event.pattern_match.group(1)
    else:
        user, reason = await get_user_from_event(event)
        if not user:
            return  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
        if user.id == jmthon.uid:
            return await edit_or_reply(event, "**... لمـاذا تࢪيـد كتم نفسـك؟ ...**")
        userid = user.id
    try:
        user = (await event.client(GetFullUserRequest(userid))).user
    except Exception:
        return await edit_or_reply(
            event, "**... غيـࢪ قـادࢪ عـلى جـلب مـعلومات الـشخص ...**"
        )
    if not is_muted(userid, "gmute"):
        return await edit_or_reply(event, f"**... هـذا الشـخص غيـࢪ مكـتوم اصلا  ...**")
    try:
        unmute(userid, "gmute")
    except Exception as e:
        await edit_or_reply(event, f"**خطـأ**\n`{e}`")
    else:
        if reason:
            await edit_or_reply(
                event,
                f"** تـم الغـاء كـتم الـمستخـدم بـنجاح  🔔، **",
            )  # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
        else:
            await edit_or_reply(
                event,
                f"** تـم الـغاء كتـم  الـمستخـدم بـنجاح  🔔، **",
            )
    if BOTLOG:
        if reason:
            await event.client.send_message(
                BOTLOG_CHATID,
                "، الغـاء الـكتم\n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n"
                f"**السبب :** `{reason}`",
            )
        else:
            await event.client.send_message(
                BOTLOG_CHATID,
                " الغـاء الـكتم \n"
                f"**المستخدم :** {_format.mentionuser(user.first_name ,user.id)} \n",
            )


# جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
# ===================================== #


@jmthon.ar_cmd(incoming=True)
async def watcher(event):
    if is_muted(event.sender_id, "gmute"):
        await event.delete()
        #########
        # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #


@jmthon.on(admin_cmd(pattern="الأحداث( -ر)?(?: |$)(\d*)?"))
async def _iundlt(event):
    rozevent = await edit_or_reply(event, "يـتم الـبحث عن اخـر الاحداث")
    flag = event.pattern_match.group(1)
    if event.pattern_match.group(2) != "":
        lim = int(event.pattern_match.group(2))
        if lim > 15:
            lim = int(15)
        if lim <= 0:
            lim = int(1)
    else:
        lim = int(5)
    adminlog = await event.client.get_admin_log(
        event.chat_id, limit=lim, edit=False, delete=True
    )
    deleted_msg = f"اخـر {lim} رسـائل مـحذوفة فـي الـدردشة :"
    if not flag:
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                deleted_msg += f"\n {msg.old.message} \n تم ارسالها بـواسطة {_format.mentionuser(ruser.first_name ,ruser.id)}"
            else:
                deleted_msg += f"\n {_media_type} \n ارسلت بـواسطـة {_format.mentionuser(ruser.first_name ,ruser.id)}"
        await edit_or_reply(rozevent, deleted_msg)
    else:
        main_msg = await edit_or_reply(rozevent, deleted_msg)
        for msg in adminlog:
            ruser = (
                await event.client(GetFullUserRequest(msg.old.from_id.user_id))
            ).user
            _media_type = media_type(msg.old)
            if _media_type is None:
                await main_msg.reply(
                    f"{msg.old.message}\nارسلت بواسطه {_format.mentionuser(ruser.first_name ,ruser.id)}"
                )
            else:
                await main_msg.reply(
                    f"{msg.old.message}\nارسلت بواسطه {_format.mentionuser(ruser.first_name ,ruser.id)}",
                    file=msg.old.media,
                )
                # جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #


# جميع الحقوق محفوظة ديربالك تخمط امك انيجها  #
@jmthon.on(admin_cmd(pattern="الغاء التثبيت( للكل|$)"))
async def pin(event):
    to_unpin = event.reply_to_msg_id
    options = (event.pattern_match.group(1)).strip()
    if not to_unpin and options != "للكل":
        return await edit_delete(
            event,
            "⌯︙يرجى الرد على الرسالة التي تريد تثبيتها استخدم `.الغاء التثبيت للكل`  لالغاء تثبيت جميع الرسائل  📍",
            5,
        )
    try:
        if to_unpin and not options:
            await event.client.unpin_message(event.chat_id, to_unpin)
        elif options == "للكل":
            await event.client.unpin_message(event.chat_id)
        else:
            return await edit_delete(
                event,
                "⌯︙يرجى الرد على الرسالة التي تريد تثبيتها استخدم `.الغاء التثبيت للكل`  لالغاء تثبيت جميع الرسائل  📍",
                5,
            )
    except BadRequestError:
        return await edit_delete(event, NO_PERM, 5)
    except Exception as e:
        return await edit_delete(event, f"`{str(e)}`", 5)
    await edit_delete(event, "**⌔ ︙تم الغاء التثبيت بنجاح  ✅**", 3)
    if BOTLOG and not event.is_private:
        await event.client.send_message(
            BOTLOG_CHATID,
            f"**⌯︙الـغاء التثبيت  ❗️ \
                \n** ⌯︙تم بنجاح الغاء التثبيـت في الدردشة  ✅ \
                \n⌔︙الدردشـه  🔖 : {event.chat.title}(`{event.chat_id}`)",
        )


"""  ماكس يابة  """
