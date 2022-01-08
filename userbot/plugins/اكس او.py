import re
from userbot import jmthon
from userbot.utils import admin_cmd

@jmthon.on(admin_cmd(pattern="اكس او$"))
# كتابة وتعديل فريق جمثون  #@hamo171002
async def gamez(event):
    if event.fwd_from:
        return
    jmusername = "@xobot"
    uunzz = "play"
    if event.reply_to_msg_id:
        await event.get_reply_message()
    tap = await bot.inline_query(jmusername, uunzz)
    await tap[0].click(event.chat_id)
    await event.delete()




IF_EMOJE = re.compile(
    "["
    "\U0001F1E0-\U0001F1FF"
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F" 
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002702-\U000027B0"
    "]+"
)


def deEmojfy(inputString: str) -> str:
    return re.sub(IF_EMOJE, "", inputString)


@jmthon.on(admin_cmd(pattern="شطرنج(?: |$)(.*)"))
async def nope(rz):
    yes = rz.pattern_match.group(1)
    if not yes:
        if rz.is_reply:
            (await rz.get_reply_message()).message

            return
    shtrnjz = await bot.inline_query("chessy_bot", f"{(deEmojfy(yes))}")
    await shtrnjz[0].click(
        rz.chat_id,
        reply_to=rz.reply_to_msg_id,
        silent=True if rz.is_reply else False,
        hide_via=True,
    )
    await rz.delete()
