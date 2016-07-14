#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os
import sys
sys.path.append(os.curdir)

# SITE INFO
AUTHOR = 'Luis Orduz'
SITENAME = 'Luis Orduz'
SITESUBTITLE = 'Thoughts on software development... mostly.'
SITEURL = ''
USER_LOGO_URL = '/assets/img/site/favicon.png'
HOSTNAME = 'luord.com'

# BASIC SETTINGS
TIMEZONE = 'America/Bogota'
DEFAULT_LANG = 'en'

# PAGING SETTINGS
DEFAULT_PAGINATION = 10
DEFAULT_DATE = 'fs'
LOCALE = ('en_US',)
SUMMARY_MAX_LENGTH = 100

# POST SETTINGS
DEFAULT_METADATA = {
    'status':'draft'
}
FILENAME_METADATA = '(?P<slug>.*)'

#FOLDER SETTINGS
PATH = 'content'
STATIC_PATHS = ['assets']
EXTRA_PATH_METADATA = {
  'assets/CNAME': {'path': 'CNAME'}
}

# SAVING SETTINGS
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}'
ARTICLE_SAVE_AS= '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
PAGE_URL = 'pages/{slug}'
CATEGORY_URL='category/{slug}'
TAG_URL='tag/{slug}'
AUTHOR_SAVE_AS=''
AUTHORS_SAVE_AS=''
AUTHOR_URL='pages/about'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# PLUGINS

PLUGINS = ['plugins.feedicon',]

# Blogroll
LINKS = (('Enter', '//enter.co'),
         ('Ars Technica', '//arstechnica.com'),
         ('FayerWayer', '//fayerwayer.com'),
         ('OSNews', '//osnews.com'),
         ('Forbes', '//forbes.com/most-popular/'),)

# Social widget
SOCIAL = (('LinkedIn', '//co.linkedin.com/in/luord'),
          ('Twitter', '//twitter.com/luord'),
          ('Facebook', '//facebook.com/luord'),
          ('IMDB', '//www.imdb.com/user/ur39224109/'),)

# THEME SETTINGS
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_POSTINFO = True
DISPLAY_CATEGORIES_ON_SUBMENU = False
TAG_CLOUD_MAX_ITEMS = 20

DISPLAY_SEARCH_FORM = True

PAGES_SORT_ATTRIBUTE = 'order'

THEME = 'theme'