#!/usr/bin/env python3

import datetime as dt
import json
import logging
import os
from typing import Literal, NamedTuple

import feedparser
import indieweb_utils as iw
import requests


MAIL_API_KEY = os.getenv("MAIL_API_KEY", "")
FEED_DELTA_DAYS = int(os.getenv("FEED_DELTA_DAYS", 1))
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

MAIL_UNSUBSCRIBE_URL = "https://luord-newsletter.web.val.run/unsubscribe"
MAIL_MESSAGE_ENDPOINT = "https://api.mailgun.net/v3/email.luord.com/messages"
MAIL_SENDER = "Luis Orduz <lo@luord.com>"
MAIL_RECIPIENT = "newsletter@email.luord.com"
MAIL_SUBJECT = "New blog post at luord.com:"
MAIL_TEMPLATE = "post"

FEED_FULL = "https://luord.com/feeds/all.atom.xml"
FEED_NOTES = "https://luord.com/feed/notes.atom.xml"

logging.basicConfig(level=logging.INFO)

if DEBUG:
    import pook
    pook.on()
    pook.enable_network("luord.com")


class Article(NamedTuple):
    title: str
    content: str
    link: str


def get_recent(feed_url: str, date_attribute: str) -> list[Article]:
    feed = feedparser.parse(feed_url)
    zone = dt.datetime.fromisoformat(feed.feed.updated).astimezone().tzinfo
    base_date = dt.datetime.now(tz=zone) - dt.timedelta(days=FEED_DELTA_DAYS)

    return [
        Article(
            title=entry.title,
            content=entry.content[0].value,
            link=entry.link
        )
        for entry in feed.entries
        if dt.datetime.fromisoformat(entry[date_attribute]) >= base_date
    ]


def send_newsletter(article: Article) -> None:
    logging.info(f"Sending newsletter for article {article.title}")

    data = {
        "from": MAIL_SENDER,
        "to": MAIL_RECIPIENT,
        "subject": f"{MAIL_SUBJECT} {article.title}",
        "template": MAIL_TEMPLATE,
        "t:variables": json.dumps(article._asdict()),
        "h:Reply-To": MAIL_SENDER,
        "h:List-Unsubscribe-Post": "List-Unsubscribe=One-Click",
        "h:List-Unsubscribe": (
            f"<{MAIL_UNSUBSCRIBE_URL}"
            "?email=%recipient_email%&ot=%recipient.id%>"
        )
    }

    try:
        response = requests.post(
            MAIL_MESSAGE_ENDPOINT,
            auth=("api", MAIL_API_KEY),
            data=data
        )
        response.raise_for_status()
    except Exception as e:
        logging.error(
            f"Failed to send newsletter for article {article.title}: {e}"
        )
        return

    logging.info(f"Sent newsletter for article {article.title}")


def send_all_newsletters() -> None:
    articles = get_recent(FEED_FULL, "published")

    for article in articles:
        send_newsletter(article)


def send_webmentions(article: Article) -> None:
    logging.info(f"Sending webmentions for {article.title}, if any")

    reply_links = iw.get_reply_urls(article.link)
    for link in reply_links:
        try:
            iw.send_webmention(article.link, link)
        except Exception as e:
            logging.error(
                f"Failed to send webmention to {link} for {article.link}: {e}"
            )
            continue

        logging.info(
            f"Sent webmention to {link} for {article.title}"
        )


def send_all_webmentions() -> None:
    articles = (
        get_recent(FEED_FULL, date_attribute="updated") +
        get_recent(FEED_NOTES, date_attribute="updated")
    )

    for article in articles:
        send_webmentions(article)


def main() -> None:
    send_all_webmentions()
    send_all_newsletters()


def single(link: str, mode: Literal["e", "w", "ew"] = "ew") -> None:
    response = requests.get(link)
    article = Article(title=link, content=response.text, link=link)

    if "w" in mode:
        send_webmentions(article)
    if "e" in mode:
        send_newsletter(article)
