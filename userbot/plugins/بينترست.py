import os
import re

import requests

from userbot import CMD_HELP, jmthon
#
try:
    from pyquery import PyQuery as pq
except ModuleNotFoundError:
    os.system("pip3 install pyquery")
    from pyquery import PyQuery as pq



def get_download_url(link):
    post_request = requests.post(
        "https://www.expertsphp.com/download.php", data={"url": link}
    )

    request_content = post_request.content
    str_request_content = str(request_content, "utf-8")
    download_url = pq(str_request_content)("table.table-condensed")("tbody")("td")(
        "a"
    ).attr("href")
    return download_url


@jmthon.on(admin_cmd(pattern="بينت?(.*)"))
@jmthon.on(sudo_cmd(pattern="بينت?(.*)", allow_sudo=True))
async def _(event):
    R = event.pattern_match.group(1)
    links = re.findall(r"\bhttps?://.*\.\S+", R)
    await event.delete()
    if not links:
        Z = await event.respond("▾∮ يجب عليك وضع رابط لتحميله")
        await asyncio.sleep(2)
        await Z.delete()
    else:
        pass
    A = await event.respond("▾∮ يتم التحميل انتظر قليلا")
    RR7PP = get_download_url(R)
    await event.client.send_file(event.chat.id, RR7PP)
    await A.delete()


CMD_HELP.update({"بينترست": "**╮•❐ الامـر ⦂** `.بينت` <رابط صورة/فيديو>\nالوظيفة ⦂ يستخدم الامر بكتابته مع رابط الصورة او الفيديو الخاص بموقع بينترست لتحميلها لك"})
