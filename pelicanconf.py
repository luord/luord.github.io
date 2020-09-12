#!/usr/bin/env python
# -*- coding: utf-8 -*- #

# SITE INFO
AUTHOR = 'Luis Orduz'
SITENAME = 'Luis Orduz'
SITESUBTITLE = 'Thoughts on software development... mostly.'
SITEURL = ''
USER_LOGO_URL = '/assets/img/site/image.png'
USER_LOGO_ICON = '/assets/img/site/favicon.png'
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

# Developer Profiles
PROFILES = (('GitLab', '//gitlab.com/luord'),
            ('GitHub', '//github.com/luord'),
            ('StackOverflow', '//stackoverflow.com/users/4570188/luis-orduz'))

# Social widget
SOCIAL = (('LinkedIn', '//linkedin.com/in/luord'),
          ('Twitter', '//twitter.com/luord'),
          ('Facebook', '//facebook.com/luord'),
          ('Hacker News', '//news.ycombinator.com/user?id=luord'),
          ('Criticker', '//www.criticker.com/profile/luord/'))

# THEME SETTINGS
DISPLAY_CATEGORIES_ON_MENU = False
DISPLAY_CATEGORIES_ON_POSTINFO = True
DISPLAY_CATEGORIES_ON_SUBMENU = False
TAG_CLOUD_MAX_ITEMS = 20

DISPLAY_SEARCH_FORM = True

PAGE_ORDER_BY = 'order'

THEME = 'theme'

PLUGIN_PATHS = ['plugins']
PLUGINS = ['feedicon', 'neighbors']
