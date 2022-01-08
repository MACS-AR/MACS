from asyncio import sleep

from googletrans import LANGUAGES, Translator

from userbot import jmthon

from ..core.managers import edit_delete, edit_or_reply
from . import deEmojify

plugin_category = "utils"


async def getTranslate(text, **kwargs):
    translator = Translator()
    result = None
    for _ in range(10):
        try:
            result = translator.translate(text, **kwargs)
        except Exception:
            translator = Translator()
            await sleep(0.1)
    return result


@jmthon.ar_cmd(
    pattern="ترجمه ([\s\S]*)",
    command=("ترجمه", plugin_category),
    info={
        "header": "To translate the text to required language.",
        "note": "For langugage codes check [this link](https://bit.ly/2SRQ6WU)",
        "usage": [
            "{tr}tl <language code> ; <text>",
            "{tr}tl <language codes>",
        ],
        "examples": "{tr}tl te ; Catuserbot is one of the popular bot",
    },
)
async def _(event):
    "To translate the text."
    input_str = event.pattern_match.group(1)
    if event.reply_to_msg_id:
        previous_message = await event.get_reply_message()
        text = previous_message.message
        lan = input_str or "en"
    elif ";" in input_str:
        lan, text = input_str.split(";")
    else:
        return await edit_delete(
            event, "⌯︙للترجمه يجـب الـرد على الرساله واكتب .ترجمه ar", time=5
        )
    text = deEmojify(text.strip())
    lan = lan.strip()
    Translator()
    try:
        translated = await getTranslate(text, dest=lan)
        after_tr_text = translated.text
        output_str = f"⌯︙تمت الترجمه مـن  : {LANGUAGES[translated.src].title()}\n ⌯︙الـى {LANGUAGES[lan].title()} \
                \n\n{after_tr_text}"
        await edit_or_reply(event, output_str)
    except Exception as exc:
        await edit_delete(event, f"**خـطأ:**\n`{str(exc)}`", time=5)
