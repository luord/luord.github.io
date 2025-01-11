#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

HOSTNAME = 'luord.com'
SITEURL = f'https://{HOSTNAME}'
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_MAX_ITEMS = 10
CATEGORY_FEED_ATOM = 'feed/{slug}.atom.xml'

NEWSLETTER_URL = 'pages/newsletter/'
NEWSLETTER_ENDPOINT = 'https://luord-newsletter.web.val.run/subscribe'

# Following items are often useful when publishing

# IndieWeb settings
WEBSUB_URL="https://luord.superfeedr.com/"
WEBMENTION_URL="https://webmention.io/luord.com/webmention"
INDIEAUTH_TOKEN="https://tokens.indieauth.com/token"
INDIEAUTH_ENDPOINT="https://indieauth.com/auth"

FEED_EXTRA_ROOT_TAGS = [
    {"name": "icon", "contents": f"{FEED_DOMAIN}/{USER_LOGO_ICON}"}
]
