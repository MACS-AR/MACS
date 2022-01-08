from . import *
from ..helpers.utils import reply_id as rd
from userbot import CMD_HELP

@bot.on(admin_cmd(pattern="المتحركات"))
@bot.on(sudo_cmd(pattern="المتحركات", allow_sudo=True))
async def gifrz(jmthon):
    await edit_or_reply(jmthon, B)

@bot.on(admin_cmd(pattern="متحركات ولد"))
@bot.on(sudo_cmd(pattern="متحركات ولد", allow_sudo=True))
async def gifrz(jmthon):
    await edit_or_reply(jmthon, ROZG)

@bot.on(admin_cmd(outgoing=True, pattern="و1$"))
@bot.on(sudo_cmd(pattern="و1$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_1:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_1, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و2$"))
@bot.on(sudo_cmd(pattern="و2$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_2:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_2, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و3$"))
@bot.on(sudo_cmd(pattern="و3$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_3:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_3, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و4$"))
@bot.on(sudo_cmd(pattern="و4$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_4:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_4, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و5$"))
@bot.on(sudo_cmd(pattern="و5$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_5:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_5, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و6$"))
@bot.on(sudo_cmd(pattern="و6$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_6:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_6, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و7$"))
@bot.on(sudo_cmd(pattern="و7$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_7:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_7, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و8$"))
@bot.on(sudo_cmd(pattern="و8$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_8:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_8, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و9$"))
@bot.on(sudo_cmd(pattern="و9$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_9:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_9, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و10$"))
@bot.on(sudo_cmd(pattern="و10$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_10:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_10, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و11$"))
@bot.on(sudo_cmd(pattern="و11$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_11:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_11, caption=jmthon_c, reply_to=roz)

@bot.on(admin_cmd(outgoing=True, pattern="و12$"))
@bot.on(sudo_cmd(pattern="و12$", allow_sudo=True))
async def GIFANIME(jmthon):
    if jmthon.fwd_from:
        return
    roz = await rd(jmthon)
    if gifrz_12:
        jmthon_c = f"**-**\n"
        await jmthon.client.send_file(jmthon.chat_id, gifrz_12, caption=jmthon_c, reply_to=roz)

CMD_HELP.update(
    {
        "متحركات":" ارسل  .المتحركات لعرض اوامر المتحركات"
    }
)
