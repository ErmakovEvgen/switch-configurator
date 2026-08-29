# Точная транслитерация по таблице P:Q из листа "Физики" Excel-конфигуратора.

TRANSLIT = {
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "sch",
    "ъ": "y",
    "ы": "y",
    "э": "e",
    "ю": "yu",
    "я": "ya",

    "А": "A",
    "Б": "B",
    "В": "V",
    "Г": "G",
    "Д": "D",
    "Е": "E",
    "Ё": "E",
    "Ж": "Zh",
    "З": "Z",
    "И": "I",
    "Й": "Y",
    "К": "K",
    "Л": "L",
    "М": "M",
    "Н": "N",
    "О": "O",
    "П": "P",
    "Р": "R",
    "С": "S",
    "Т": "T",
    "У": "U",
    "Ф": "F",
    "Х": "Kh",
    "Ц": "Ts",
    "Ч": "Ch",
    "Ш": "Sh",
    "Щ": "Sch",
    "Ы": "Y",
    "Э": "E",
    "Ю": "Yu",
    "Я": "Ya",
}


def transliterate(text: str) -> str:
    result = text

    # Excel выполняет SUBSTITUTE последовательно.
    for source, target in TRANSLIT.items():
        result = result.replace(source, target)

    return result


def fio_to_description(fio: str) -> str:
    transliterated = transliterate(fio.strip())
    parts = transliterated.split()

    if not parts:
        return ""

    surname = parts[0]
    name_initial = parts[1][0] if len(parts) >= 2 else ""
    patronymic_initial = parts[2][0] if len(parts) >= 3 else ""

    return f"{surname}{name_initial}{patronymic_initial}"