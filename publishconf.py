#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

HOSTNAME = 'luord.com'
SITEURL = 'https://' + HOSTNAME
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_MAX_ITEMS = 30

WEBSUB_URL="https://luord.superfeedr.com/"

# Following items are often useful when publishing

# SOCIAL SETTINGS
FACEBOOK_USERNAME = "luord"
LINKEDIN_USERNAME = "luis-orduz"
TWITTER_USERNAME="luord"

FEED_EXTRA_ROOT_TAGS = [
    {"name": "link", "attrs": {"rel": "hub", "href": WEBSUB_URL}},
    {"name": "icon", "contents": f"{SITEURL}{USER_LOGO_ICON}"}
]
