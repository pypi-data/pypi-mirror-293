#!/usr/bin/env python
# -*- coding: utf-8 -*-

# soyjak.party URL generator. Inherit and override this for derivative classes  (e.g. 420chan API, 8chan/vichan API)
class Url(object):
    # default value for board in case user wants to query board list
    def __init__(self, board_name, https=False):
        self._board_name = board_name
        self._protocol = 'https://' if https else 'http://'

        # soyjak.party API URL Subdomains
        DOMAIN = {
            'api': self._protocol + 'soyjak.party',   # API subdomain
            'boards': self._protocol + 'soyjak.party', # HTML subdomain
            'raid': self._protocol + 'soyak.party', # HTML subdomain
            'file': self._protocol + 'soyjak.party',  # file (image) host
            #'file': self._protocol + 'soyjak.party', # new, slower image host
            'thumbs': self._protocol + 'soyjak.party',# thumbs host
            'static': self._protocol + 'soyjak.party' # static host
        }

        # soyjak.party API URL Templates
        TEMPLATE = {
            'api': {  # URL structure templates
                'board': DOMAIN['api'] + '/{board}/{page}.json',
                'thread': DOMAIN['api'] + '/{board}/thread/{thread_id}.json'
            },
            'http': { # Standard HTTP viewing URLs
                'board': DOMAIN['boards'] + '/{board}/{page}',
                'thread': DOMAIN['boards'] + '/{board}/thread/{thread_id}'
            },
            'data': {
                'file': DOMAIN['file'] + '/{board}/src/{tim}{ext}',
                'thumbs': DOMAIN['thumbs'] + '/{board}/thumb/{tim}{ext}',
                'static': DOMAIN['static'] + '/image/{item}'
            }
        }

        # soyjak.party API Listings
        LISTING = {
            'board_list': DOMAIN['api'] + '/boards.json',
            'thread_list': DOMAIN['api'] + '/{board}/threads.json',
            'catalog': DOMAIN['api'] + '/{board}/catalog.json'
        }

        # combine all dictionaries into self.URL dictionary
        self.URL = TEMPLATE
        self.URL.update({'domain': DOMAIN})
        self.URL.update({'listing': LISTING})

    # generate boards listing URL
    def board_list(self):
        return self.URL['listing']['board_list']

    # generate board page URL
    def page_url(self, page):
        return self.URL['api']['board'].format(
            board=self._board_name,
            page=page
            )

    # generate catalog URL
    def catalog(self):
        return self.URL['listing']['catalog'].format(
            board=self._board_name
            )

    # generate threads listing URL
    def thread_list(self):
        return self.URL['listing']['thread_list'].format(
            board=self._board_name
            )

#    # generate archived threads list URL (disabled for compatibility)
#    def archived_thread_list(self):
#        return self.URL['listing']['archived_thread_list'].format(
#            board=self._board_name
#            )

    # generate API thread URL
    def thread_api_url(self, thread_id):
        return self.URL['api']['thread'].format(
            board=self._board_name,
            thread_id=thread_id
            )

    # generate HTTP thread URL
    def thread_url(self, thread_id):
        return self.URL['http']['thread'].format(
            board=self._board_name,
            thread_id=thread_id
            )

    # generate file URL
    def file_url(self, tim, ext):
        return self.URL['data']['file'].format(
            board=self._board_name,
            tim=tim,
            ext=ext
            )

    # generate thumb URL
    def thumb_url(self, tim, ext):
        return self.URL['data']['thumbs'].format(
            board=self._board_name,
            tim=tim,
            ext=ext
            )

    # return entire URL dictionary
    @property
    def site_urls(self):
        return self.URL