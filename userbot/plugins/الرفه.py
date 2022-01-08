import random
from Jmthon.razan.resources.strings import *
from userbot import jmthon, CMD_HELP
from userbot import jmthon
from ..core.managers import edit_or_reply
from ..helpers import get_user_from_event

@jmthon.on(admin_cmd(pattern="نسبة الرجولة(?: |$)(.*)"))
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if user.id == 1293312980:
        return await edit_or_reply(mention, f"**100%**")
    if user.id == 1293312980:
        return await edit_or_reply(mention, f"**100%**")
    if user.id == 1293312980:
        return await edit_or_reply(mention, f"**100%**")
    muh = user.first_name.replace("\u2060", "") if user.first_name else user.username
    sos = random.choice(kz)
    await edit_or_reply(
        mention, f"- نسبة الرجولة لـ [{muh}](tg://user?id={user.id}) هـي {sos} 🥵🖤"
    )

@jmthon.on(admin_cmd(pattern="رفع حيوان(?: |$)(.*)"))
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention, f"- المستخدم [{tag}](tg://user?id={user.id}) \n- تـم رفعـه حيوان 🐏"
    )

@jmthon.on(admin_cmd(pattern="رفع بزون(?: |$)(.*)"))
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention, f"- المستخدم [{tag}](tg://user?id={user.id}) \n- تـم رفعـه بزون 🐈"
    )

@jmthon.on(admin_cmd(pattern="رفع زاحف(?: |$)(.*)"))
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention, f"- المستخدم [{tag}](tg://user?id={user.id}) \n- تـم رفعـه زاحف 🐍💞"
    )
@jmthon.on(admin_cmd(pattern="رفع زبي(?: |$)(.*)"))
async def permalink(mention):
    user, custom = await get_user_from_event(mention)
    if not user:
        return
    if custom:
        return await edit_or_reply(mention, f"[{custom}](tg://user?id={user.id})")
    tag = user.first_name.replace("\u2060", "") if user.first_name else user.username
    await edit_or_reply(
        mention, f"- المستخدم [{tag}](tg://user?id={user.id}) \n- تـم رفعـه علي زبك 😂🖕"
    )

