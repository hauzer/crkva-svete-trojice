from transliterate import translit
from slugify import slugify


def slugify_sr_cyrl(title):
    return slugify(translit(title, language_code='sr', reversed=True))
