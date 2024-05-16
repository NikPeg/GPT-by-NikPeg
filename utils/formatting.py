import re


def escape_symbols(s):
    s = re.escape(s)
    s = re.sub(r'\!', '\!', s)
    s = re.sub(r'\=', '\=', s)
    s = re.sub(r'\`', '\`', s)
    s = re.sub(r'\<', '\<', s)
    s = re.sub(r'\>', '\>', s)
    s = re.sub(r'\+', '\+', s)
    return s


def escape_markdown_symbols(s):
    # Заменяем заголовки
    s = re.sub(r"^### (.*?)\n", r"*\1*\n", s)
    s = re.sub(r"\n### (.*?)\n", r"\n*\1*\n", s)
    s = re.sub(r"\n### (.*?)\n", r"\n*\1*\n", s)
    s = re.sub(r"\n### (.*?)$", r"\n*\1*", s)
    s = re.sub(r"^### (.*?)$", r"\n*\1*", s)

    characters_to_escape = set("!@#$%^&()+-={}\\[]./")
    escaped_string = ''.join(['\\' + char if char in characters_to_escape else char for char in s])
    return escaped_string


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
    s = re.sub(r"^### (.*?)$", r"\n<b>\1</b>", s)

    return s
