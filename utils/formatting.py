import re


def screen_symbols(s):
    s = re.sub(r'\}', r'\\}', s)
    s = re.sub(r'\@', r'\\@', s)
    s = re.sub(r'\#', r'\\#', s)
    s = re.sub(r'\$', r'\\$', s)
    s = re.sub(r'\%', r'\\%', s)
    s = re.sub(r'\&', r'\\&', s)
    s = re.sub(r"\*", "\*", s)
    return s


def screen_markdownv2_symbols(s):
    s = re.sub(r'\}', r'\\}', s)
    s = re.sub(r'\@', r'\\@', s)
    s = re.sub(r'\.', r'\\.', s)
    s = re.sub(r'\!', r'\\!', s)
    s = re.sub(r'\#', r'\\#', s)
    s = re.sub(r'\$', r'\\$', s)
    s = re.sub(r'\%', r'\\%', s)
    s = re.sub(r'\&', r'\\&', s)
    s = re.sub(r'\-', r'\\-', s)
    return s


def markdown_to_html(s):
    # Сначала заменяем **жирный** текст
    s = re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", s)
    # Затем заменяем *курсивный* текст
    s = re.sub(r"\*(.*?)\*", r"<i>\1</i>", s)

    # Заменяем заголовки
    s = re.sub(r"^### (.*?)\n", r"<b>\1</b>\n", s)
    s = re.sub(r"\n### (.*?)\n", r"\n<b>\1</b>\n", s)
    s = re.sub(r"\n### (.*?)\n", r"\n<b>\1</b>\n", s)
    s = re.sub(r"\n### (.*?)$", r"\n<b>\1</b>", s)

    return s
