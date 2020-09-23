#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

HOSTNAME = 'luord.com'
SITEURL = '//' + HOSTNAME
RELATIVE_URLS = False

FEED_DOMAIN = SITEURL
FEED_ALL_ATOM = 'feeds/all.atom.xml'
FEED_MAX_ITEMS = 30

# Following items are often useful when publishing

# EXTERNAL SETTINGS
DISQUS_SITENAME='luord'
GOOGLE_ANALYTICS = "UA-74953282-1"

# TODO: GitHub, PiWik, Gaug.es

# SOCIAL SETTINGS
FACEBOOK_USERNAME = "luord"
LINKEDIN_USERNAME = "luis-orduz"
TWITTER_USERNAME="luord"
SHARETHIS_ID = "5dba6e805940d400134b17b2"
