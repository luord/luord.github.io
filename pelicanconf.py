#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# SITE INFO
AUTHOR = 'Luis Orduz'
AUTHOR_EMAIL = 'lo@luord.com'
SITENAME = 'Luis Orduz'
SITESUBTITLE = 'Software Engineer, occasional writer, and movie watcher.'
SITEDESCRIPTION = 'Software Engineering, Python, and life.'
SITEURL = ''
USER_LOGO_URL = 'assets/img/site/image.png'
USER_LOGO_ICON = 'assets/img/site/favicon.png'
HOSTNAME = ''

# BASIC SETTINGS
TIMEZONE = 'America/Bogota'
DEFAULT_LANG = 'en'

# PAGING SETTINGS
DEFAULT_PAGINATION = 10
PAGINATION_PATTERNS = (
    (1, '{url}', '{save_as}'),
    (2, '{base_name}/p/{number}', '{base_name}/p/{number}.html'),
)
DEFAULT_DATE = None
SUMMARY_MAX_LENGTH = 100

# POST SETTINGS
DEFAULT_METADATA = {
    'status':'draft'
}
FILENAME_METADATA = '(?P<slug>.*)'
SUMMARY_MAX_LENGTH = 20

#FOLDER SETTINGS
PATH = 'content'
STATIC_PATHS = ['assets']
EXTRA_PATH_METADATA = {
  'assets/CNAME': {'path': 'CNAME'},
  'assets/redirect/resume.html': {'path': 'pages/resume.html'},
  'assets/redirect/email.html': {'path': 'pages/email/index.html', 'url': 'pages/email/'},
}

# SAVING SETTINGS
ARTICLE_URL = '{date:%Y}/{date:%m}/{date:%d}/{slug}/'
ARTICLE_SAVE_AS= '{date:%Y}/{date:%m}/{date:%d}/{slug}/index.html'
ARTICLE_EXCLUDES = ['assets']
PAGE_URL = 'pages/{slug}/'
PAGE_SAVE_AS = 'pages/{slug}/index.html'
CATEGORY_URL='category/{slug}/'
CATEGORY_SAVE_AS='category/{slug}/index.html'
TAG_URL='tag/{slug}/'
TAG_SAVE_AS='tag/{slug}/index.html'
ARCHIVES_URL='archives/'
ARCHIVES_SAVE_AS='archives/index.html'
CATEGORIES_URL='categories/'
CATEGORIES_SAVE_AS='categories/index.html'
TAGS_URL='tags/'
TAGS_SAVE_AS='tags/index.html'
AUTHOR_SAVE_AS=''
AUTHORS_SAVE_AS=''
AUTHOR_URL=''
CONTACT_URL='pages/contact/'
ABOUT_URL='pages/about/'
MISSION_URL='pages/work/'

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
    "Notes": "Random thoughts in short format."
}

HASHED_CATEGORIES = ("Notes",)

MENUITEMS = (
    ("Notes", "category/notes/"),
)

PLUGIN_PATHS = ['plugins']
PLUGINS = ['article_hasher', 'category_separator', 'feed_extra_root', 'neighbors', 'sitemap']
