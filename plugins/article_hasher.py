import base64

from pelican import signals


def get_b32_hash(stamp):
    alphabet = b"234567abcdefghijklmnopqrstuvwxyz"
    bytestamp = int(stamp).to_bytes(4, 'big')
    return base64._b32encode(alphabet, bytestamp).decode().rstrip("=")


def hash_urls(generator):
    for article in generator.articles:
        if article.category not in generator.context["HASHED_CATEGORIES"]:
            continue

        b32_hash = get_b32_hash(article.date.timestamp())
        article.ix = b32_hash
        article.override_save_as = f"{article.category.slug}/{b32_hash}/index.html"
        article.override_url = f"{article.category.slug}/{b32_hash}/"


def register():
    signals.article_generator_pretaxonomy.connect(hash_urls)
