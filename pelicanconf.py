#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# SITE INFO
AUTHOR = 'Luis Orduz'
AUTHOR_EMAIL = 'lo@luord.com'
SITENAME = 'Luis Orduz'
SITESUBTITLE = 'Software Engineer'
SITEDESCRIPTION = 'Thoughts on software engineering and architecture.'
SITEURL = ''
USER_LOGO_URL = 'assets/img/site/image.png'
USER_LOGO_ICON = 'assets/img/site/favicon.png'
HOSTNAME = ''

# BASIC SETTINGS
TIMEZONE = 'America/Bogota'
DEFAULT_LANG = 'en'

# PAGING SETTINGS
DEFAULT_PAGINATION = 10
DEFAULT_DATE = 'fs'
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
  'assets/CNAME': {'path': 'CNAME'},
  'assets/redirect/resume.html': {'path': 'pages/resume.html'}
}

# SAVING SETTINGS
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}'
ARTICLE_SAVE_AS= '{date:%Y}/{date:%m}/{date:%d}/{slug}.html'
ARTICLE_EXCLUDES = ['assets']
PAGE_URL = 'pages/{slug}'
CATEGORY_URL='category/{slug}'
TAG_URL='tag/{slug}'
AUTHOR_SAVE_AS=''
AUTHORS_SAVE_AS=''
AUTHOR_URL=''
CONTACT_URL='pages/contact'
ABOUT_URL='pages/about'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = ""
CATEGORY_FEED_ATOM = ""
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# THEME SETTINGS
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_POSTINFO = True
DISPLAY_CATEGORIES_ON_SUBMENU = False
TAG_CLOUD_MAX_ITEMS = 20

PAGE_ORDER_BY = 'order'

THEME = 'theme'

SKIPPED_CATEGORIES = ("Notes",)

CATEGORY_DESCRIPTIONS = {
    "Notes": "Here I post random thoughts in short format. Excluded from the main feed."
}

MENUITEMS = (
    ("Notes", "category/notes"),
)

PLUGIN_PATHS = ['plugins']
PLUGINS = ['category_separator', 'feed_extra_root', 'neighbors']
