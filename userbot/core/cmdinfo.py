from typing import Dict, List, Union

from ..helpers.utils.extdl import install_pip

try:
    from urlextract import URLExtract
except ModuleNotFoundError:
    install_pip("urlextract")
    from urlextract import URLExtract

from ..Config import Config

extractor = URLExtract()


def get_data(about, type):
    data = about[type]
    urls = extractor.find_urls(data)
    if len(urls) > 0:
        return data
    return data.capitalize()


def _format_about(
    about: Union[str, Dict[str, Union[str, List[str], Dict[str, str]]]]
) -> str:  # sourcery no-metrics
    if not isinstance(about, dict):
        return about
    tmp_chelp = ""
    if "header" in about and isinstance(about["header"], str):
        tmp_chelp += f"{about['header'].title()}"
        del about["header"]
    if "description" in about and isinstance(about["description"], str):
        tmp_chelp += "\n\n▾∮  **الشـرح :**\n" f"{get_data(about , 'description')}"
        del about["description"]
    if "flags" in about:
        tmp_chelp += "\n\n▾∮  **الأضـافات الـمتاحـة :**"
        if isinstance(about["flags"], dict):
            for f_n, f_d in about["flags"].items():
                tmp_chelp += f"\n    ▫ `{f_n}` : {f_d.lower()}"
        else:
            tmp_chelp += f"\n    {about['flags']}"
        del about["flags"]
    if "options" in about:
        tmp_chelp += "\n\n▾∮  **الخـيارات الـمتـاحة :**"
        if isinstance(about["options"], dict):
            for o_n, o_d in about["options"].items():
                tmp_chelp += f"\n    ▫ `{o_n}` : {o_d.lower()}"
        else:
            tmp_chelp += f"\n    {about['options']}"
        del about["options"]
    if "types" in about:
        tmp_chelp += "\n\n▾∮  **Supported Types :**"
        if isinstance(about["types"], list):
            for _opt in about["types"]:
                tmp_chelp += f"\n    `{_opt}` ,"
        else:
            tmp_chelp += f"\n    {about['types']}"
        del about["types"]
    if "usage" in about:
        tmp_chelp += "\n\n▾∮  **الأسـتخـدام :**"
        if isinstance(about["usage"], list):
            for ex_ in about["usage"]:
                tmp_chelp += f"\n    `{ex_}`"
        else:
            tmp_chelp += f"\n    `{about['usage']}`"
        del about["usage"]
    if "examples" in about:
        tmp_chelp += "\n\n▾∮  **امثـلة توضـيحيـة :**"
        if isinstance(about["examples"], list):
            for ex_ in about["examples"]:
                tmp_chelp += f"\n    `{ex_}`"
        else:
            tmp_chelp += f"\n    `{about['examples']}`"
        del about["examples"]
    if "others" in about:
        tmp_chelp += f"\n\n▾∮  **الأخـرى :**\n{get_data(about , 'others')}"
        del about["others"]
    if about:
        for t_n, t_d in about.items():
            tmp_chelp += f"\n\n▾∮  **{t_n.title()} :**\n"
            if isinstance(t_d, dict):
                for o_n, o_d in t_d.items():
                    tmp_chelp += f"    ▫ `{o_n}` : {get_data(t_d , o_n)}\n"
            elif isinstance(t_d, list):
                for _opt in t_d:
                    tmp_chelp += f"    `{_opt}` ,"
                tmp_chelp += "\n"
            else:
                tmp_chelp += f"{get_data(about ,t_n)}"
                tmp_chelp += "\n"
    return tmp_chelp.replace("{tr}", Config.COMMAND_HAND_LER)
