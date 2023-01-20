from pelican import signals


def separate(article_generator):
    if not article_generator.context.get("SKIPPED_CATEGORIES"):
        return

    article_generator.hidden_articles += [
        article for article in article_generator.articles
        if article.category.name in article_generator.context["SKIPPED_CATEGORIES"]
    ]

    article_generator.articles = [
        article for article in article_generator.articles
        if article.category.name not in article_generator.context["SKIPPED_CATEGORIES"]
    ]


def register():
    signals.article_generator_finalized.connect(separate)
