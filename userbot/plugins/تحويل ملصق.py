
from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError
from userbot import jmthon
from userbot.utils import admin_cmd


@jmthon.on(admin_cmd(pattern="تحويل لملصق ?(.*)"))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.edit("**- يـجب الرد علـى رسـالة الـمستخدم***")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.text:
        await event.edit("-** يـجب. الرد علـى رسـالة الـمستخدم **")
        return
    chat = "@QuotLyBot"
    reply_message.sender
    if reply_message.sender.bot:
        await event.edit("يـجب. الرد علـى رسـالة الـمستخدم )")
        return
    await event.edit("جار تحويل النص الى ملصق")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1031952739)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await event.reply("```Please unblock me (@QuotLyBot) u Nigga```")
            return
        if response.text.startswith("Hi!"):
            await event.edit("يجـب الغاء خصـوصية التوجيـه اولا")
        else:
            await event.delete()
            await event.client.send_message(event.chat_id, response.message)



