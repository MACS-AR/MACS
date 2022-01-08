"""الاوامـر : .وضع بايو, .وضع صورة, .وضع اسم, .حذف صورة.،  انشائي"""

import os

from telethon.tl import functions
from telethon.tl.functions.channels import GetAdminedPublicChannelsRequest
from telethon.tl.functions.photos import DeletePhotosRequest, GetUserPhotosRequest
from telethon.tl.types import InputPhoto

from userbot import jmthon, CMD_HELP
#
from ..Config import Config
from ..core.managers import edit_delete, edit_or_reply


@jmthon.on(admin_cmd(pattern="وضع بايو (.*)"))
async def _(event):
    if event.fwd_from:
        return
    brzo = event.pattern_match.group(1)
    try:
        await jmthon(functions.account.UpdateProfileRequest(about=brzo))
        await event.edit("**- تم تغيير البايو بنجاح ✓**")
    except Exception as z:
        await event.edit(str(z))


@jmthon.on(admin_cmd(pattern="وضع اسم ((.|\n)*)"))
async def _(event):
    if event.fwd_from:
        return
    rozname = event.pattern_match.group(1)
    first_name = rozname
    last_name = ""
    if "\\n" in rozname:
        first_name, last_name = rozname.split("\\n", 1)
    try:
        await jmthon(
            functions.account.UpdateProfileRequest(
                first_name=first_name, last_name=last_name
            )
        )
        await event.edit("**- تم تغيير الاسـم بنجاح ✓**")
    except Exception as z:
        await event.edit(str(z))


@jmthon.on(admin_cmd(pattern="وضع صورة"))
async def _(event):
    if event.fwd_from:
        return
    reply_message = await event.get_reply_message()
    await event.edit("**- يتم تحميل الصورة الى بيانات السورس 💞**")
    if not os.path.isdir(Config.TMP_DOWNLOAD_DIRECTORY):
        os.makedirs(Config.TMP_DOWNLOAD_DIRECTORY)
    photo = None
    try:
        photo = await jmthon.download_media(
            reply_message, Config.TMP_DOWNLOAD_DIRECTORY
        )
    except Exception as z:
        await event.edit(str(z))
    else:
        if photo:
            await event.edit("**• يتم الرفع علر التيليجرام .  .  .**")
            file = await jmthon.upload_file(photo)
            try:
                await jmthon(functions.photos.UploadProfilePhotoRequest(file))
            except Exception as z:
                await event.edit(str(z))
            else:
                await event.edit("**- تم تغيير صورة الحساب الشخصي بنجاح ✓**")
    try:
        os.remove(photo)
    except Exception as z:
        logger.warn(str(z))


@jmthon.on(admin_cmd(pattern="حذف صورة ?(.*)"))
async def remove_profilepic(delpfp):
    group = delpfp.text[8:]
    if group == "all":
        lim = 0
    elif group.isdigit():
        lim = int(group)
    else:
        lim = 1
    pfplist = await delpfp.client(
        GetUserPhotosRequest(user_id=delpfp.sender_id, offset=0, max_id=0, limit=lim)
    )
    input_photos = [
        InputPhoto(
            id=sep.id,
            access_hash=sep.access_hash,
            file_reference=sep.file_reference,
        )
        for sep in pfplist.photos
    ]
    await delpfp.client(DeletePhotosRequest(id=input_photos))
    await edit_delete(delpfp, f"⌔∮ تم حذف صـورة من صور حسابك بنجاح ✅")


@jmthon.on(admin_cmd(pattern="انشائي$"))
async def _(event):
    result = await event.client(GetAdminedPublicChannelsRequest())
    output_str = "- جميع القنوات والمجموعات التي قمت بأنشائها :\n"
    output_str += "".join(
        f" - {channel_obj.title} @{channel_obj.username} \n"
        for channel_obj in result.chats
    )
    await edit_or_reply(event, output_str)
CMD_HELP.update(
    {
        "الحساب": "• .وضع بايو <بايو>\n     لتغيير البايو الخاص بحسابك اكتب الامر وبايو\
         \n\n• .وضع اسم <اسم>\n     لتغيير اسم حسابك الشخصي اكتب الامر واسمك\
         \n\n• .وضع صورة (رد على صورة)\n      لتغيير صورة حسابك الشخصية بالرد على الصورة التي تريدها\
         \n\n• .انشائي\n فقط ارسل الامر لعرض القنوات والمجموعات التي انشئتها\
         \n\n• .حذف صورة <عدد>(اختياري العدد)\n    لحذف صورة لك حسابك الشخصي اذا ما حددت عدد راح يحذف صورة فقط"
    }
)