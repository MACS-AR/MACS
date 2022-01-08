import asyncio

from userbot import CMD_HELP, jmthon
from userbot.utils import admin_cmd

#
@jmthon.on(admin_cmd(pattern=r"(.*)", outgoing=True))
async def _(event):

    if event.fwd_from:

        return

    animation_interval = 2

    animation_ttl = range(0, 11)

    input_str = event.pattern_match.group(1)

    if input_str == "تهكير":

        await event.edit(input_str)

        animation_chars = [
            "▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `",
            "█████████████████████▒▒▒▒ `",
            "█████████████████████████ `",
            "- تم اختراق الضيحه وارسال جميع معلوماته في الرسائل المحفوظة\n\n فحبيبي اذا تحب اذا تبقى تكمز كل شي يمي\n\n#ترفيه",
        ]

        for i in animation_ttl:

            await asyncio.sleep(animation_interval)

            await event.edit(animation_chars[i % 11])


CMD_HELP.update({"تهكير": ".تهكير \nفقط ارسل الامر الترفيه"})

