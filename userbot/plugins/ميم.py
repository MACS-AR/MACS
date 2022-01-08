import asyncio

from userbot import jmthon

from ..core.managers import edit_or_reply

plugin_category = "fun"


@jmthon.ar_cmd(
    pattern="^\:/$",
    command=("\:", plugin_category),
    info={
        "header": "امر المتحركات",
        "usage": "\:",
    },
)
async def kek(keks):
    "امر المتحركات"
    keks = await edit_or_reply(keks, ":\\")
    uio = ["/", "\\"]
    for i in range(15):
        await asyncio.sleep(0.5)
        txt = ":" + uio[i % 2]
        await keks.edit(txt)


@jmthon.ar_cmd(
    pattern="^\-_-$",
    command=("-_-", plugin_category),
    info={
        "header": "امر المتحركات",
        "usage": "-_-",
    },
)
async def lol(lel):
    "Animation command"
    lel = await edit_or_reply(lel, "-__-")
    okay = "-__-"
    for _ in range(15):
        await asyncio.sleep(0.5)
        okay = okay[:-1] + "_-"
        await lel.edit(okay)


@jmthon.ar_cmd(
    pattern="^\;_;$",
    command=(";_;", plugin_category),
    info={
        "header": "امر المتحركات",
        "usage": ";_;",
    },
)
async def fun(e):
    "امر المتحركات"
    e = await edit_or_reply(e, ";__;")
    t = ";__;"
    for _ in range(15):
        await asyncio.sleep(0.5)
        t = t[:-1] + "_;"
        await e.edit(t)


@jmthon.ar_cmd(
    pattern="هفف$",
    command=("هفف", plugin_category),
    info={
        "header": "امر المتحركات",
        "usage": "{tr}هفف",
    },
)
async def Oof(e):
    "امر المتحركات"
    t = "ۿـفف"
    catevent = await edit_or_reply(e, t)
    for _ in range(15):
        await asyncio.sleep(0.5)
        t = t[:-1] + "ۿـف"
        await catevent.edit(t)


@jmthon.ar_cmd(
    pattern="فصخ ([\s\S]*)",
    command=("فصخ", plugin_category),
    info={
        "header": "الكتابة المتقطعة",
        "usage": "{tr}النص",
    },
)
async def typewriter(typew):
    "Type writter animation."
    message = typew.pattern_match.group(1)
    sleep_time = 0.2
    typing_symbol = "|"
    old_text = ""
    typew = await edit_or_reply(typew, typing_symbol)
    await asyncio.sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit(typing_text)
        await asyncio.sleep(sleep_time)
        await typew.edit(old_text)
        await asyncio.sleep(sleep_time)


@jmthon.ar_cmd(
    pattern="عيد (\d*) ([\s\S]*)",
    command=("عيد", plugin_category),
    info={
        "header": "تكرار النص المحدد مع عدد معين من المرات",
        "usage": "{tr}عيد <العدد> <النص>",
        "examples": "{tr}عيد 10 جمثون",
    },
)
async def _(event):
    "لتكرار النص المحدد."
    cat = ("".join(event.text.split(maxsplit=1)[1:])).split(" ", 1)
    message = cat[1]
    count = int(cat[0])
    repsmessage = (f"{message} ") * count
    await edit_or_reply(event, repsmessage)


@jmthon.ar_cmd(
    pattern="meme",
    command=("meme", plugin_category),
    info={
        "header": "امر المتحركات",
        "usage": [
            "{tr}meme <ايموجي/نص>",
            "{tr}meme",
        ],
    },
)
async def meme(event):
    "امر المتحركات"
    memeVar = event.text
    sleepValue = 0.5
    memeVar = memeVar[6:]
    if not memeVar:
        memeVar = "✈️"
    event = await edit_or_reply(event, "-------------" + memeVar)
    await asyncio.sleep(sleepValue)
    await event.edit("------------" + memeVar + "-")
    await asyncio.sleep(sleepValue)
    await event.edit("-----------" + memeVar + "--")
    await asyncio.sleep(sleepValue)
    await event.edit("----------" + memeVar + "---")
    await asyncio.sleep(sleepValue)
    await event.edit("---------" + memeVar + "----")
    await asyncio.sleep(sleepValue)
    await event.edit("--------" + memeVar + "-----")
    await asyncio.sleep(sleepValue)
    await event.edit("-------" + memeVar + "------")
    await asyncio.sleep(sleepValue)
    await event.edit("------" + memeVar + "-------")
    await asyncio.sleep(sleepValue)
    await event.edit("-----" + memeVar + "--------")
    await asyncio.sleep(sleepValue)
    await event.edit("----" + memeVar + "---------")
    await asyncio.sleep(sleepValue)
    await event.edit("---" + memeVar + "----------")
    await asyncio.sleep(sleepValue)
    await event.edit("--" + memeVar + "-----------")
    await asyncio.sleep(sleepValue)
    await event.edit("-" + memeVar + "------------")
    await asyncio.sleep(sleepValue)
    await event.edit(memeVar + "-------------")
    await asyncio.sleep(sleepValue)
    await event.edit("-------------" + memeVar)
    await asyncio.sleep(sleepValue)
    await event.edit("------------" + memeVar + "-")
    await asyncio.sleep(sleepValue)
    await event.edit("-----------" + memeVar + "--")
    await asyncio.sleep(sleepValue)
    await event.edit("----------" + memeVar + "---")
    await asyncio.sleep(sleepValue)
    await event.edit("---------" + memeVar + "----")
    await asyncio.sleep(sleepValue)
    await event.edit("--------" + memeVar + "-----")
    await asyncio.sleep(sleepValue)
    await event.edit("-------" + memeVar + "------")
    await asyncio.sleep(sleepValue)
    await event.edit("------" + memeVar + "-------")
    await asyncio.sleep(sleepValue)
    await event.edit("-----" + memeVar + "--------")
    await asyncio.sleep(sleepValue)
    await event.edit("----" + memeVar + "---------")
    await asyncio.sleep(sleepValue)
    await event.edit("---" + memeVar + "----------")
    await asyncio.sleep(sleepValue)
    await event.edit("--" + memeVar + "-----------")
    await asyncio.sleep(sleepValue)
    await event.edit("-" + memeVar + "------------")
    await asyncio.sleep(sleepValue)
    await event.edit(memeVar + "-------------")
    await asyncio.sleep(sleepValue)
    await event.edit(memeVar)


@jmthon.ar_cmd(
    pattern="give",
    command=("give", plugin_category),
    info={
        "header": "امر المتحركات",
        "usage": [
            "{tr}give <اموجي/نص>",
            "{tr}give",
        ],
    },
)
async def give(event):
    "امر المتحركات"
    giveVar = event.text
    sleepValue = 0.5
    lp = giveVar[6:]
    if not lp:
        lp = " 🍭"
    event = await edit_or_reply(event, lp + "        ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + "       ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + "      ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + "     ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + "    ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + "   ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + "  ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + " ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + lp)
    await asyncio.sleep(sleepValue)
    await event.edit(lp + "        ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + "       ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + "      ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + "     ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + "    ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + "   ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + "  ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + " ")
    await asyncio.sleep(sleepValue)
    await event.edit(lp + lp + lp + lp + lp + lp + lp + lp + lp)


@jmthon.ar_cmd(
    pattern="sadmin$",
    command=("sadmin", plugin_category),
    info={
        "header": "صياح ب امر متحركة الادمن",
        "usage": "{tr}sadmin",
    },
)
async def _(event):
    "صياح ب امر متحركة الادمن"
    animation_ttl = range(13)
    event = await edit_or_reply(event, "sadmin")
    animation_chars = [
        "@aaaaaaaaaaaaadddddddddddddmmmmmmmmmmmmmiiiiiiiiiiiiinnnnnnnnnnnnn",
        "@aaaaaaaaaaaaddddddddddddmmmmmmmmmmmmiiiiiiiiiiiinnnnnnnnnnnn",
        "@aaaaaaaaaaadddddddddddmmmmmmmmmmmiiiiiiiiiiinnnnnnnnnnn",
        "@aaaaaaaaaaddddddddddmmmmmmmmmmiiiiiiiiiinnnnnnnnnn",
        "@aaaaaaaaadddddddddmmmmmmmmmiiiiiiiiinnnnnnnnn",
        "@aaaaaaaaddddddddmmmmmmmmiiiiiiiinnnnnnnn",
        "@aaaaaaadddddddmmmmmmmiiiiiiinnnnnnn",
        "@aaaaaaddddddmmmmmmiiiiiinnnnnn",
        "@aaaaadddddmmmmmiiiiinnnnn",
        "@aaaaddddmmmmiiiinnnn",
        "@aaadddmmmiiinnn",
        "@aaddmmiinn",
        "@admin",
    ]
    for i in animation_ttl:
        await asyncio.sleep(1)
        await event.edit(animation_chars[i % 13])
