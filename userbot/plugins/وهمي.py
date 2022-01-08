import asyncio
import time

import aiohttp
from telethon.errors import ChatAdminRequiredError as no_admin
from telethon.tl.functions.messages import ExportChatInviteRequest

from Jmthon.razan.resources.strings import *
from userbot import jmthon
from userbot.utils import admin_cmd

from ..core.managers import edit_or_reply
from ..core.managers import edit_or_reply as eod
from ..helpers import get_user_from_event
from . import *
import os
B =  """
┏━━┓┏━━┓┏━━┓┏━━┓
┗━┓┃┃┏┓┃┗━┓┃┗━┓┃
┏━┛┃┃┃┃┃┏━┛┃┏━┛┃
HAPPY NEW YEAR 2022
┃┗━┓┃┗┛┃┃┗━┓┃┗━┓
┗━━┛┗━━┛┗━━┛┗━━┛"""

@jmthon.on(admin_cmd(pattern="2022"))
async def _(muhammad):
       await muhammad.edit(B)


@jmthon.on(admin_cmd(pattern="كتابة(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("**- يجب كتابة الامر بشكل صحيح**")
    await event.edit(f"**تم بدء وضع الكتابة الوهمية لـ {t} من الثوانـي**")
    async with event.client.action(event.chat_id, "typing"):
        await asyncio.sleep(t)


@jmthon.on(admin_cmd(pattern="صوتية(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("**- يجب كتابة الامر بشكل صحيح**")
    await event.edit(f"**تم بدء وضع ارسال الصوتية الوهمية لـ {t} من الثوانـي**")
    async with event.client.action(event.chat_id, "record-audio"):
        await asyncio.sleep(t)


@jmthon.on(admin_cmd(pattern="فيد(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("**- يجب كتابة الامر بشكل صحيح**")
    await event.edit(f"**تم بدء وضع ارسال الفيديو الوهمي لـ {t} من الثوانـي**")
    async with event.client.action(event.chat_id, "record-video"):
        await asyncio.sleep(t)


@jmthon.on(admin_cmd(pattern="لعبة(?: |$)(.*)"))
async def _(event):
    t = event.pattern_match.group(1)
    if not (t or t.isdigit()):
        t = 100
    else:
        try:
            t = int(t)
        except BaseException:
            try:
                t = await event.ban_time(t)
            except BaseException:
                return await event.edit("**- يجب كتابة الامر بشكل صحيح**")
    await event.edit(f"**تم بدء وضع اللعب الوهمي لـ {t} من الثوانـي**")
    async with event.client.action(event.chat_id, "game"):
        await asyncio.sleep(t)


@jmthon.on(admin_cmd(pattern="الرابط$"))
async def _(e):
    rr = await edit_or_reply(e, "**يتم جلب الرابط انتظر **")
    try:
        r = await e.client(
            ExportChatInviteRequest(e.chat_id),
        )
    except no_admin:
        return await eod(rr, "عذرا انت لست مشرف في هذه الدردشة", time=10)
    await eod(rr, f"- رابط الدردشة\n {r.link}")


@jmthon.on(admin_cmd(pattern="للكل تاك$"))
async def listall(jmthon):
    if jmthon.fwd_from:
        return
    mentions = "- هذه هي قائمة جميع الاعضاء هنا: "
    chat = await bot.get_input_chat()
    async for x in borg.iter_participants(chat, 2000):
        mentions += f" \n[{x.first_name}](tg://user?id={x.id})"
    await jmthon.reply(mentions)
    await jmthon.delete()




@jmthon.on(admin_cmd(pattern="نزوج(?:\s|$)([\s\S]*)"))
async def rzfun(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 1293312980:
        return await edit_or_reply(mention, f"**لا عيني محمد يحب بنية 😂🤍**")
    await edit_or_reply(mention, f"**نزوج وماتباوع على غيري 🥺💞 ܰ**")


@jmthon.on(admin_cmd(pattern="طلاك(?:\s|$)([\s\S]*)"))
async def mention(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 1293312980:
        return await edit_or_reply(mention, f"**لا عيني محمد يحب بنية 😂🤍**")
    await edit_or_reply(mention, f"**طالق طالق بالعشرة 😹😭💕 ܰ**")


@jmthon.on(admin_cmd(pattern="طقس (.*)"))
@jmthon.on(sudo_cmd(pattern="طقس (.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    Key = "f806cebbd44f34cc4cd1d79a290081be"  # ايبي مالتي تخمط اهينك 😭😹💕
    sample_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"
    input_str = event.pattern_match.group(1)
    async with aiohttp.ClientSession() as session:
        response_api_zero = await session.get(sample_url.format(input_str, Key))
    response_api = await response_api_zero.json()
    if response_api["cod"] == 200:
        country_code = response_api["sys"]["country"]
        country_time_zone = int(response_api["timezone"])
        sun_rise_time = int(response_api["sys"]["sunrise"]) + country_time_zone
        sun_set_time = int(response_api["sys"]["sunset"]) + country_time_zone
        await edit_or_reply(
            event,
            """{}
-**الحـرارة**: {}°С
-**درجة الحرارة الصغرى:** {}°С
-**درجة الحرارة العظم:** {}°С
**الرطـوبة**: {}%
-**الـرياح**: {}m/s
-**السحـاب**: {}hpa
-**شروق الشمس**: {} {}
-**غروب الشمس**: {} {}""".format(
                input_str,
                response_api["main"]["temp"],
                response_api["main"]["temp_min"],
                response_api["main"]["temp_max"],
                response_api["main"]["humidity"],
                response_api["wind"]["speed"],
                response_api["clouds"]["all"],
                # response_api["main"]["pressure"],
                time.strftime("%Y-%m-%d %I:%M:%S", time.gmtime(sun_rise_time)),
                country_code,
                time.strftime("%Y-%m-%d %I:%M:%S", time.gmtime(sun_set_time)),
                country_code,
            ),
        )
    else:
        await edit_or_reply(event, response_api["message"])


import asyncio

from jmthon.utils import admin_cmd

from userbot import jmthon

R = (
    "┈┈╱▔▔▔▔▔▔▔▔▔▔▔▏\n"
    "┈╱╭▏╮╭┻┻╮╭┻┻╮╭▏ \n"
    "▕╮╰▏╯┃╭╮┃┃╭╮┃╰▏ \n"
    "▕╯┈▏┈┗┻┻┛┗┻┻┻╮▏ \n"
    "▕╭╮▏╮┈┈┈┈┏━━━╯▏\n"
    "▕╰╯▏╯╰┳┳┳┳┳┳╯╭▏ \n"
    "▕┈╭▏╭╮┃┗┛┗┛┃┈╰▏ \n"
    "▕┈╰▏╰╯╰━━━━╯┈┈▏\n"
)


@jmthon.on(admin_cmd(pattern=r"سبونج"))
async def kerz(kerz):
    await kerz.edit(R)

    A = (
        "╭━┳━╭━╭━╮╮\n"
        "┃┈┈┈┣▅╋▅┫┃\n"
        "┃┈┃┈╰━╰━━━━━━╮\n"
        "╰┳╯┈┈┈┈┈┈┈┈┈◢▉◣\n"
        "╲┃┈┈┈┈┈┈┈┈┈┈▉▉▉\n"
        "╲┃┈┈┈┈┈┈┈┈┈┈◥▉◤\n"
        "╲┃┈┈┈┈╭━┳━━━━╯\n"
        "╲┣━━━━━━┫\n"
    )


@jmthon.on(admin_cmd(pattern=r"كلب"))
async def dog(dog):
    await dog.edit(A)
    Z = (
        "┈┏━╮╭━┓┈╭━━━━╮\n"
        "┈┃┏┗┛┓┃╭┫ⓞⓘⓝⓚ┃\n"
        "┈╰┓▋▋┏╯╯╰━━━━╯\n"
        "╭━┻╮╲┗━━━━╮╭╮┈\n"
        "┃▎▎┃╲╲╲╲╲╲┣━╯┈\n"
        "╰━┳┻▅╯╲╲╲╲┃┈┈┈\n"
        "┈┈╰━┳┓┏┳┓┏╯┈┈┈\n"
        "┈┈┈┈┗┻┛┗┻┛┈┈┈┈\n"
    )


A = (
    " ╱▏┈┈┈┈┈┈▕╲▕╲┈┈┈\n"
    "▏▏┈┈┈┈┈┈▕▏▔▔╲┈┈\n"
    "▏╲┈┈┈┈┈┈╱┈▔┈▔╲┈\n"
    "╲▏▔▔▔▔▔▔╯╯╰┳━━▀\n"
    "┈▏╯╯╯╯╯╯╯╯╱┃┈┈┈\n"
    "┈┃┏┳┳━━━┫┣┳┃┈┈┈\n"
    "┈┃┃┃┃┈┈┈┃┃┃┃┈┈┈\n"
    "┈┗┛┗┛┈┈┈┗┛┗┛┈┈┈\n"
)

A = (
    "┈┈┈┈╱▔▔▔▔▔╲┈╱▔╲\n"
    "┈┈┈┈▏┈┈▏╭╮▕┈▏╳▕\n"
    "┈┈┈┈▏┈┈▏┈┈▕┈╲▂╱\n"
    "┈╱▔▔╲▂╱╲▂▂┈╲▂▏▏\n"
    "╭▏┈┈┈┈┈┈┈▏╲▂▂╱┈\n"
    "┃▏┈┈┈┈▏┈┈▏┈┈┈┈┈\n"
    "╯▏┈╲╱▔╲▅▅▏┈┈┈┈\n"
    "┈╲▅▅▏▕▔▔▔▔▏┈┈┈┈\n"
)

N = (
    "┈┈┈╭━━━━━╮┈┈┈┈┈\n"
    "┈┈┈┃┊┊┊┊┊┃┈┈┈┈┈\n"
    "┈┈┈┃┊┊╭━╮┻╮┈┈┈┈\n"
    "┈┈┈╱╲┊┃▋┃▋┃┈┈┈┈\n"
    "┈┈╭┻┊┊╰━┻━╮┈┈┈┈\n"
    "┈┈╰┳┊╭━━━┳╯┈┈┈┈\n"
    "┈┈┈┃┊┃╰━━┫┈┈┈┈\n"
    "┈┈┈┈┈┈┏━┓┈┈┈┈┈┈\n"
)


@jmthon.on(admin_cmd(pattern=r"ذئب"))
async def fox(fox):
    await fox.edit(A)


@jmthon.on(admin_cmd(pattern=r"فيل"))
async def elephant(elephant):
    await elephant.edit(A)


@jmthon.on(admin_cmd(pattern=r"هومر"))
async def homer(homer):
    await homer.edit(N)


@jmthon.on(admin_cmd(pattern=r"بك"))
async def pig(pig):
    await pig.edit(Z)
