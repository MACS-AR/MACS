from telethon import *

from userbot import *
from userbot.utils import *

from .. import jmthon


@jmthon.ar_cmd(pattern="اسمه")
async def rz(event):
    reply = await event.get_reply_message()
    if not reply:
        await event.edit("- يجب الرد على اي مستخدم لنسخ اسمه .")
        return
    a = await bot.get_entity(reply.sender_id)
    b = f"`{a.first_name}`"
    await event.respond(b)


@jmthon.ar_cmd(pattern="معرفه ?(.*)")
async def rz(event):
    ty = event.pattern_match.group(1)
    await event.edit("- يتم التعرف")
    if not ty:
        await event.edit("يجب وضع ايدي المستخدم للحصول على معرفه")
        return
    a = await bot.get_entity(int(ty))
    if not a:
        await event.edit("Your id is invalid")
        return
    b = a.username
    c = f"المعرف هو  :  "
    if not b:
        await event.edit("- ايدي المستخدم غير صالح")
        return
    await event.respond(f"{c}@{b}")


@jmthon.ar_cmd(pattern="التكرار")
async def rz(event):
    for h in range(10000):
        ab = await event.get_reply_message()
        if ab.media:
            bc = ab
            await bot.send_message(event.chat_id, file=bc)
        else:
            c = ab.text
            dc = c
            await bot.send_message(event.chat_id, dc)


@jmthon.on(admin_cmd(pattern="رسائلي"))
async def _(event):
    a = await bot.get_messages(event.chat_id, 0, from_user="me")
    await event.edit(f"- مجموع رسائلك في المجموعة هي  {a.total}")


@jmthon.on(admin_cmd(pattern="رسائل الكروب"))
async def _(event):
    b = await bot.get_messages(event.chat_id)
    await event.edit(f"- مجموع الرسائل في المجموعة هي  {b.total}")


@jmthon.ar_cmd(pattern="رقمه")
async def rzp(event):
    a = "+"
    reply = await event.get_reply_message()
    if not reply:
        await event.edit("- يجب الرد على المستخدم")
        return
    b = await bot.get_entity(reply.sender_id)
    c = b.phone
    if not c:
        await event.edit(
            "عذرا لا استطيع ايجاد رقم هذا الحساب يبدو انه ليس في جهات الاتصال"
        )
        return
    d = c.replace(c, a + c)
    await bot.send_message(event.chat_id, f"- رقم حساب المستخدم هو : {d}")
