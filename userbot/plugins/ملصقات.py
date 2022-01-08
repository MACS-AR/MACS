import asyncio
import base64
import io
import math
import urllib.request
from os import remove
from telethon.tl.functions.stickers import SuggestShortNameRequest
import emoji as catemoji
from PIL import Image
from telethon.tl import functions, types
from telethon.utils import get_input_document
from telethon.tl.functions.messages import GetStickerSetRequest
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import (
    DocumentAttributeFilename,
    DocumentAttributeSticker,
    InputStickerSetID,
    MessageMediaPhoto,
)

from userbot import jmthon

from ..core.managers import edit_delete, edit_or_reply
from ..helpers.tools import media_type
from ..sql_helper.globals import gvarstatus

plugin_category = "fun"

# modified and developed by @MACS37


combot_stickers_url = "https://combot.org/telegram/stickers?q="

EMOJI_SEN = [
    "Можно отправить несколько смайлов в одном сообщении, однако мы рекомендуем использовать не больше одного или двух на каждый стикер.",
    "You can list several emoji in one message, but I recommend using no more than two per sticker",
    "يمكنك إرسال قائمة بعدة رموز في رسالة واحدة، لكن أنصحك بعدم إرسال أكثر من رمزين للملصق الواحد.",
    "Du kannst auch mehrere Emoji eingeben, ich empfehle dir aber nicht mehr als zwei pro Sticker zu benutzen.",
    "Você pode listar vários emojis em uma mensagem, mas recomendo não usar mais do que dois por cada sticker.",
    "Puoi elencare diverse emoji in un singolo messaggio, ma ti consiglio di non usarne più di due per sticker.",
    "emoji",
]

KANGING_STR = [
    "**⌯︙انتظر يتم صنع الملصق*",
]


def verify_cond(catarray, text):
    return any(i in text for i in catarray)


def pack_name(userid, pack, is_anim):
    if is_anim:
        return f"JMTHONBOT_{userid}_{pack}_anim"
    return f"JMTHON_{userid}_{pack}"


def char_is_emoji(character):
    return character in catemoji.UNICODE_EMOJI["en"]


def pack_nick(username, pack, is_anim):
    if gvarstatus("CUSTOM_STICKER_PACKNAME"):
        if is_anim:
            packnick = (
                f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} حقـوق.{pack} (Animated)"
            )
        else:
            packnick = f"{gvarstatus('CUSTOM_STICKER_PACKNAME')} حقـوق.{pack}"
    elif is_anim:
        packnick = f"@{username} حقـوق.{pack} (Animated)"
    else:
        packnick = f"@{username} حقـوق.{pack}"
    return packnick


async def resize_photo(photo):
    """Resize the given photo to 512x512"""
    image = Image.open(photo)
    if (image.width and image.height) < 512:
        size1 = image.width
        size2 = image.height
        if image.width > image.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        image = image.resize(sizenew)
    else:
        maxsize = (512, 512)
        image.thumbnail(maxsize)
    return image


async def newpacksticker(
    catevent,
    conv,
    cmd,
    args,
    pack,
    packnick,
    stfile,
    emoji,
    packname,
    is_anim,
    otherpack=False,
    pkang=False,
):
    await conv.send_message(cmd)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packnick)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        remove("AnimatedSticker.tgs")
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
    rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.text):
        await catevent.edit(
            f"فشل اضافة الملصق ، استخدم بوت الملصقات @Stickers لأضافة الملصق يدويا.\n**خطأ :**{rsp}"
        )
        return
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/publish")
    if is_anim:
        await conv.get_response()
        await conv.send_message(f"<{packnick}>")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message("/skip")
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message(packname)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return otherpack, packname, emoji
    return pack, packname


async def add_to_pack(
    catevent,
    conv,
    args,
    packname,
    pack,
    userid,
    username,
    is_anim,
    stfile,
    emoji,
    cmd,
    pkang=False,
):
    await conv.send_message("/addsticker")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.send_message(packname)
    x = await conv.get_response()
    while ("50" in x.text) or ("120" in x.text):
        try:
            val = int(pack)
            pack = val + 1
        except ValueError:
            pack = 1
        packname = pack_name(userid, pack, is_anim)
        packnick = pack_nick(username, pack, is_anim)
        await catevent.edit(f"** تبديل الحـزمة الى {str(pack)} بسبب امتلاء الحزمة")
        await conv.send_message(packname)
        x = await conv.get_response()
        if x.text == "**الحـزمة المحددة غير صحيحة**":
            return await newpacksticker(
                catevent,
                conv,
                cmd,
                args,
                pack,
                packnick,
                stfile,
                emoji,
                packname,
                is_anim,
                otherpack=True,
                pkang=pkang,
            )
    if is_anim:
        await conv.send_file("AnimatedSticker.tgs")
        remove("AnimatedSticker.tgs")
    else:
        stfile.seek(0)
        await conv.send_file(stfile, force_document=True)
    rsp = await conv.get_response()
    if not verify_cond(EMOJI_SEN, rsp.text):
        await catevent.edit(
            f"⌯︙فشل اضافة الملصق ، استخدم بوت الملصقات @Stickers لأضافة الملصق يدويا.\n**خطأ :**{rsp}"
        )
        return
    await conv.send_message(emoji)
    await args.client.send_read_acknowledge(conv.chat_id)
    await conv.get_response()
    await conv.send_message("/done")
    await conv.get_response()
    await args.client.send_read_acknowledge(conv.chat_id)
    if not pkang:
        return packname, emoji
    return pack, packname


@jmthon.ar_cmd(
    pattern="ملصق(?:\s|$)([\s\S]*)",
    command=("ملصق", plugin_category),
)
async def kang(args):
    "jmthon userbot"
    photo = None
    emojibypass = False
    is_anim = False
    emoji = None
    message = await args.get_reply_message()
    user = await args.client.get_me()
    if not user.username:
        try:
            user.first_name.encode("utf-8").decode("ascii")
            username = user.first_name
        except UnicodeDecodeError:
            username = f"rz_{user.id}"
    else:
        username = user.username
    userid = user.id
    if message and message.media:
        if isinstance(message.media, MessageMediaPhoto):
            rozevent = await edit_or_reply(args, f"-  يتم اضافة الملصق الى الحزمة")
            photo = io.BytesIO()
            photo = await args.client.download_media(message.photo, photo)
        elif "image" in message.media.document.mime_type.split("/"):
            rozevent = await edit_or_reply(args, f"-  يتم اضافة الملصق الى الحزمة")
            photo = io.BytesIO()
            await args.client.download_file(message.media.document, photo)
            if (
                DocumentAttributeFilename(file_name="sticker.webp")
                in message.media.document.attributes
            ):
                emoji = message.media.document.attributes[1].alt
                emojibypass = True
        elif "tgsticker" in message.media.document.mime_type:
            rozevent = await edit_or_reply(args, f"-  يتم اضافة الملصق الى الحزمة")
            await args.client.download_file(
                message.media.document, "AnimatedSticker.tgs"
            )

            attributes = message.media.document.attributes
            for attribute in attributes:
                if isinstance(attribute, DocumentAttributeSticker):
                    emoji = attribute.alt
            emojibypass = True
            is_anim = True
            photo = 1
        else:
            await edit_delete(args, "- الملف غير مدعوم")
            return
    else:
        await edit_delete(args, "-  لا استطيع اخذ هذا الملصق")
        return
    if photo:
        splat = ("".join(args.text.split(maxsplit=1)[1:])).split()
        emoji = emoji if emojibypass else "🤍"
        pack = 1
        if len(splat) == 2:
            if char_is_emoji(splat[0][0]):
                if char_is_emoji(splat[1][0]):
                    return await rozevent.edit("تأكد من الامر بشكل صحيح")
                pack = splat[1]
                emoji = splat[0]
            elif char_is_emoji(splat[1][0]):
                pack = splat[0]
                emoji = splat[1]
            else:
                return await rozevent.edit("تأكد من الامر بشكل صحيح")
        elif len(splat) == 1:
            if char_is_emoji(splat[0][0]):
                emoji = splat[0]
            else:
                pack = splat[0]
        packnick = pack_nick(username, pack, is_anim)
        packname = pack_name(userid, pack, is_anim)
        cmd = "/newpack"
        stfile = io.BytesIO()
        if is_anim:
            cmd = "/newanimated"
        else:
            image = await resize_photo(photo)
            stfile.name = "sticker.png"
            image.save(stfile, "PNG")
        response = urllib.request.urlopen(
            urllib.request.Request(f"http://t.me/addstickers/{packname}")
        )
        htmlstr = response.read().decode("utf8").split("\n")
        if (
            "  A <strong>Telegram</strong> user has created the <strong>Sticker&nbsp;Set</strong>."
            not in htmlstr
        ):
            async with args.client.conversation("@Stickers") as conv:
                packname, emoji = await add_to_pack(
                    rozevent,
                    conv,
                    args,
                    packname,
                    pack,
                    userid,
                    username,
                    is_anim,
                    stfile,
                    emoji,
                    cmd,
                )
            if packname is None:
                return
            await edit_delete(
                rozevent,
                f"-  تم بنجاح اخذ الملصق \
                    \n الحزمة الخاصة بك هي  [اضغط هنا](t.me/addstickers/{packname}) و الايموجي الخاص هز {emoji}",
                parse_mode="md",
                time=10,
            )
        else:
            await rozevent.edit("- يتم احضار حزمة جديدة")
            async with args.client.conversation("@Stickers") as conv:
                otherpack, packname, emoji = await newpacksticker(
                    rozevent,
                    conv,
                    cmd,
                    args,
                    pack,
                    packnick,
                    stfile,
                    emoji,
                    packname,
                    is_anim,
                )
            if otherpack is None:
                return
            if otherpack:
                await edit_delete(
                    rozevent,
                    f"-  تم بنجاح اخذ الملصق لحزمة ثانيـة\
                    \n الحزمة الخاصة بك هي  [اضغط هنا](t.me/addstickers/{packname}) و الايموجي الخاص هز {emoji}",
                    parse_mode="md",
                    time=10,
                )
            else:
                await edit_delete(
                    rozevent,
                    f"-  تم بنجاح اخذ الملصق \
                    \n الحزمة الخاصة بك هي  [اضغط هنا](t.me/addstickers/{packname}) و الايموجي الخاص هز {emoji}",
                    parse_mode="md",
                    time=10,
                )


@jmthon.on(admin_cmd(pattern="حزمة"))
async def jmthonpkg(_):
    roz = await _.get_reply_message()
    if not roz:
        return await edit_or_reply(_, "**- يجب عليك الرد على حزمة  .**")
    if len(_.text) > 9:
        _packname = _.text.split(" ", maxsplit=1)[1]
    else:
        _packname = f"{_.sender_id}"
    _id = roz.media.document.attributes[1].stickerset.id
    _hash = roz.media.document.attributes[1].stickerset.access_hash
    _get_stiks = await _.client(
        functions.messages.GetStickerSetRequest(
            stickerset=types.InputStickerSetID(id=_id, access_hash=_hash)
        )
    )
    stiks = []
    for i in _get_stiks.documents:
        jmt = get_input_document(i)
        stiks.append(
            types.InputStickerSetItem(
                document=jmt,
                emoji=(i.attributes[1]).alt,
            )
        )
    try:
        short_name = (await _.client(SuggestShortNameRequest(_packname))).short_name
        jmthon_roz = await bot(
            functions.stickers.CreateStickerSetRequest(
                user_id=_.sender_id,
                title=_packname,
                short_name=f"u{short_name}_by_{bot.me.username}",
                stickers=stiks,
            )
        )
    except BaseException as er:
        LOGS.exception(er)
        return await edit_or_reply(_, str(er))
    await edit_or_reply(
        _, f"**- تم اخذ الحزمه بنجاح ✓ \nالحزمه  → [اضغط هنا](https://t.me/addstickers/{jmthon_roz.set.short_name})**")


@jmthon.ar_cmd(
    pattern="معلومات_الملصق$",
    command=("معلومات_الملصق", plugin_category),
    info={
        "header": "To get information about a sticker pick.",
        "description": "Gets info about the sticker packk",
        "usage": "{tr}stkrinfo",
    },
)
async def get_pack_info(event):
    "To get information about a sticker pick."
    if not event.is_reply:
        return await edit_delete(
            event, "`لا أستطيع إحضار المعلومات من لا شيء ، هل يمكنني ذلك ؟!`", 5
        )
    rep_msg = await event.get_reply_message()
    if not rep_msg.document:
        return await edit_delete(
            event, "**⌯︙هاذا ليس ملصق يجب الرد على الملصق اولا**", 5
        )
    try:
        stickerset_attr = rep_msg.document.attributes[1]
        catevent = await edit_or_reply(
            event, "**⌯︙إحضار تفاصيل حزمة الملصقات ، يُرجى الانتظار**`"
        )
    except BaseException:
        return await edit_delete(
            event, "**⌯︙هذا ليس ملصق يجب الرد على الملصق اولا**", 5
        )
    if not isinstance(stickerset_attr, DocumentAttributeSticker):
        return await catevent.edit("**⌯︙هذا ليس ملصق يجب الرد على الملصق اولا.**")
    get_stickerset = await event.client(
        GetStickerSetRequest(
            InputStickerSetID(
                id=stickerset_attr.stickerset.id,
                access_hash=stickerset_attr.stickerset.access_hash,
            )
        )
    )
    pack_emojis = []
    for document_sticker in get_stickerset.packs:
        if document_sticker.emoticon not in pack_emojis:
            pack_emojis.append(document_sticker.emoticon)
    OUTPUT = (
        f"**⌯︙عنوان الملصق:** `{get_stickerset.set.title}\n`"
        f"**⌯︙الاسم القصير للملصق:** `{get_stickerset.set.short_name}`\n"
        f"**⌯︙المـسؤل:** `{get_stickerset.set.official}`\n"
        f"**⌯︙الارشيف:** `{get_stickerset.set.archived}`\n"
        f"**⌯︙حزمة الملصق:** `{get_stickerset.set.count}`\n"
        f"**⌯︙الايموجي المستخدم:**\n{' '.join(pack_emojis)}"
    )
    await catevent.edit(OUTPUT)
