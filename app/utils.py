from transliterate import slugify


def ru2en_transliteration(text: str) -> str:
    return slugify(text)