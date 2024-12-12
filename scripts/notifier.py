#!/usr/bin/env python3

import datetime as dt
import json
import logging
import os
from types import SimpleNamespace
from typing import Literal

import feedparser
import indieweb_utils as iw
import requests


MAIL_API_KEY = os.getenv("MAIL_API_KEY", "")
MAIL_UNSUBSCRIBE_URL = os.getenv(
    "MAIL_UNSUBSCRIBE_URL",
    "https://luord-newsletter.web.val.run/unsubscribe"
)
MAIL_MESSAGE_ENDPOINT = os.getenv(
    "MAIL_MESSAGE_ENDPOINT",
    "https://api.mailgun.net/v3/email.luord.com/messages"
)
MAIL_SENDER = os.getenv("MAIL_SENDER", "Luis Orduz <lo@luord.com>")
MAIL_RECIPIENT = os.getenv("MAIL_RECIPIENT", "newsletter@email.luord.com")
MAIL_SUBJECT = os.getenv("MAIL_SUBJECT", "New blog post at luord.com:")
MAIL_TEMPLATE = os.getenv("MAIL_TEMPLATE", "post")

FEED_FULL = os.getenv("FEED_FULL", "https://luord.com/feeds/all.atom.xml")
FEED_NOTES = os.getenv("FEED_NOTES", "https://luord.com/feed/notes.atom.xml")
FEED_DELTA_DAYS = int(os.getenv("FEED_DELTA_DAYS", 1))


logging.basicConfig(level=logging.INFO)


def get_new_items(
    feed_url: str, date_attribute: str = 'published'
) -> list[feedparser.util.FeedParserDict]:
    feed = feedparser.parse(feed_url)
    zone = dt.datetime.fromisoformat(feed.feed.updated).astimezone().tzinfo
    base_date = dt.datetime.now(tz=zone) - dt.timedelta(days=FEED_DELTA_DAYS)

    return [
        entry
        for entry in feed.entries
        if dt.datetime.fromisoformat(entry[date_attribute]) >= base_date
    ]


def send_newsletter(items: list[feedparser.util.FeedParserDict]) -> None:
    for item in items:
        logging.info(f"Sending newsletter for item {item.title}")

        data = {
            "from": MAIL_SENDER,
            "to": MAIL_RECIPIENT,
            "subject": f"{MAIL_SUBJECT} {item.title}",
            "template": MAIL_TEMPLATE,
            "t:variables": json.dumps({
                "title": item.title,
                "content": item.content[0].value,
                "link": item.link
            }),
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
        except requests.exceptions.HTTPError as e:
            logging.error(
                f"Failed to send newsletter for item {item.title}: {e}"
            )
            logging.error(response.text)
            continue

        logging.info(f"Sent newsletter for item {item.title}")


def send_webmentions(items: list[feedparser.util.FeedParserDict]) -> None:
    for item in items:
        logging.info(f"Sending webmentions for {item.title}, if any")

        reply_links = iw.get_reply_urls(item.link)
        for link in reply_links:
            try:
                iw.send_webmention(item.link, link)
            except Exception as e:
                logging.error(
                    f"Failed to send webmention to {link} for {item.link}: {e}"
                )
                continue

            logging.info(
                f"Sent webmention to {link} for {item.title}"
            )


def main() -> None:
    logging.info(f"Getting items for last {FEED_DELTA_DAYS} days")

    full_items = get_new_items(FEED_FULL)
    note_items = get_new_items(FEED_NOTES, date_attribute="updated")

    send_newsletter(full_items)
    send_webmentions(full_items + note_items)


def single(link: str, mode: Literal["e", "w", "ew"] = "ew") -> None:
    response = requests.get(link)
    item = SimpleNamespace(
        content=[SimpleNamespace(value=response.text)],
        link=link,
        title=link
    )

    if "w" in mode:
        send_webmentions([item])
    if "e" in mode:
        send_newsletter([item])


if __name__ == "__main__":
    import pook
    from fire import Fire
    pook.on()
    pook.enable_network("luord.com")
    Fire()
    pook.off()
