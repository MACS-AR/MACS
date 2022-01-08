import logging

from userbot.utils import admin_cmd

from userbot import CMD_HELP, jmthon

logger = logging.getLogger(__name__)

#
if 1 == 1:
    name = "Profile Photos"
    client = borg

    @jmthon.on(admin_cmd(pattern="صورة(.*)"))
    @jmthon.on(sudo_cmd(pattern="صورة(.*)", allow_sudo=True))
    async def potocmd(event):
        id = "".join(event.raw_text.split(maxsplit=2)[1:])
        user = await event.get_reply_message()
        chat = event.input_chat
        if user:
            photos = await event.client.get_profile_photos(user.sender)
        else:
            photos = await event.client.get_profile_photos(chat)
        if id.strip() == "":
            try:
                await event.client.send_file(event.chat_id, photos)
            except a:
                photo = await event.client.download_profile_photo(chat)
                await borg.send_file(event.chat_id, photo)
        else:
            try:
                id = int(id)
                if id <= 0:
                    await eor(event, "**- ايدي المستخدم الذي وضعته غير صالح .**")
                    return
            except BaseException:
                await eor(event, "هاه؟ ")
                return
            if int(id) <= (len(photos)):
                send_photos = await event.client.download_media(photos[id - 1])
                await borg.send_file(event.chat_id, send_photos)
            else:
                await eor(event, "⌔∮ هذا المستخدم ليس لديه صور")
                return


CMD_HELP.update(
    {
        "الصورة": "**╮•❐ الامر ⦂** `.صورة` <عدد الصور (اختياري)> <بالرد على الشخص>\nالوظيفة ⦂ لأخذ صورة حساب شخص معين بالرد عليه بالامر"
    }
)
