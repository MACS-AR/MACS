# ترجمه فريق ماكس على التيلكرام
import json

import requests

# ترجمه فريق ماكس على التيلكرام
from . import edit_delete, edit_or_reply, jmthon

plugin_category = "extra"

# ترجمه فريق ماكس على التيلكرام
@jmthon.ar_cmd(
    pattern="صلاة(?: |$)(.*)",
    command=("صلاة", plugin_category),
    info={
        "header": "Shows you the Islamic prayer times of the given city name.",
        "note": "you can set default city by using {tr}setcity command.",
        "usage": "{tr}صلاه <المحافظه>",
        "examples": "{tr}صلاه baghdad ",
    },
)
async def get_adzan(adzan):
    LOKASI = adzan.pattern_match.group(1)
    url = f"https://api.pray.zone/v2/times/today.json?city={LOKASI}"
    request = requests.get(url)
    if request.status_code != 200:
        await edit_delete(
            adzan,
            f"** لم يـتم العثور على معلومات لـهذه المدينه {LOKASI}**\n يرجى كتابة اسم محافظتك وباللغه الانكليزي ",
            5,
        )  # ترجمه فريق ماكس على التيلكرام
        return
    result = json.loads(request.text)
    jmthonresult = f"<b>اوقـات صـلاه المـسلمين 👳‍♂️ </b>\
            \n\n<b>المـدينة     : </b><i>{result['results']['location']['city']}</i>\
            \n<b>الـدولة  : </b><i>{result['results']['location']['country']}</i>\
            \n<b>التـاريخ     : </b><i>{result['results']['datetime'][0]['date']['gregorian']}</i>\
            \n<b>الهـجري    : </b><i>{result['results']['datetime'][0]['date']['hijri']}</i>\
            \n\n<b>الامـساك    : </b><i>{result['results']['datetime'][0]['times']['Imsak']}</i>\
            \n<b>شـروق الشمس  : </b><i>{result['results']['datetime'][0]['times']['Sunrise']}</i>\
            \n<b>الـفجر     : </b><i>{result['results']['datetime'][0]['times']['Fajr']}</i>\
            \n<b>الضـهر    : </b><i>{result['results']['datetime'][0]['times']['Dhuhr']}</i>\
            \n<b>العـصر      : </b><i>{result['results']['datetime'][0]['times']['Asr']}</i>\
            \n<b>غـروب الشمس   : </b><i>{result['results']['datetime'][0]['times']['Sunset']}</i>\
            \n<b>المـغرب  : </b><i>{result['results']['datetime'][0]['times']['Maghrib']}</i>\
            \n<b>العشـاء     : </b><i>{result['results']['datetime'][0]['times']['Isha']}</i>\
            \n<b>منتـصف الليل : </b><i>{result['results']['datetime'][0]['times']['Midnight']}</i>\
    "
    await edit_or_reply(adzan, jmthonresult, "html")


