from userbot import CMD_HELP
from userbot import jmthon

GCAST_BLACKLIST = [
    -1001118102804,
    -1001161919602,
    ]
#

@jmthon.on(admin_cmd(pattern="للكروبات(?: |$)(.*)"))
async def gcast(event):
    jmthon = event.pattern_match.group(1)
    if jmthon:
        msg = jmthon
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await eor(event, "**-يجب الرد على رسالو او وسائط او كتابه النص مع الامر**")
        return
    roz = await edit_or_reply(event, "⌔∮ يتم الاذاعة في الخاص انتظر لحضه")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_group:
            chat = x.id
            try:
                if chat not in GCAST_BLACKLIST:
                    await event.client.send_message(chat, msg)
                    done += 1
            except BaseException:
                er += 1
    await roz.edit(
        f"**- تم بنجاح الأذاعة الى ** `{done}` **من الدردشات ، خطأ في ارسال الى ** `{er}` **من الدردشات**"
    )
    
@jmthon.on(admin_cmd(pattern="للخاص(?: |$)(.*)"))
async def gucast(event):
    jmthon = event.pattern_match.group(1)
    if jmthon:
        msg = jmthon
    elif event.is_reply:
        msg = await event.get_reply_message()
    else:
        await eor(event, "**-يجب الرد على رسالو او وسائط او كتابه النص مع الامر**")
        return
    roz = await edit_or_reply(event, "⌔∮ يتم الاذاعة في الخاص انتظر لحضه")
    er = 0
    done = 0
    async for x in event.client.iter_dialogs():
        if x.is_user and not x.entity.bot:
            chat = x.id
            try:
                done += 1
                await event.client.send_message(chat, msg)
            except BaseException:
                er += 1
    await roz.edit(
        f"**- تم بنجاح الأذاعة الى ** `{done}` **من الدردشات ، خطأ في ارسال الى ** `{er}` **من الدردشات**"
    )
    
    
CMD_HELP.update(
    {
      "الاذاعه": "**الامر: **`.للكروبات`<نص/بالرد ؏ ميديا> \
        \n  •  **الوظيفة : **لعمل اذاعه في المجموعات لرسالة معينه او تستطيع بالرد على صورة او ملصق او الخ\
        \n\n **الامر:** `.للخاص <نص/بالرد ؏ ميديا>` \
        \n •  **الوظيفة  :** لعمل اذاعه لرسالة او صورة بالرد ؏ الشي التريد توسليه اذاعه بالامر "
    }
)
