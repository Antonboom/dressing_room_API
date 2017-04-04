# -*- coding: utf-8 -*-

import os
import random
import gzip
import urllib

from urllib import request
from urllib.parse import urlencode

from user_agent import generate_user_agent

from .utils import HtmlSoup

"""
Proxy sources:
    https://hidemy.name/en/proxy-list/?maxtime=1500&type=h&anon=3#list
    http://proxyserverlist-24.blogspot.ru
"""


class CategoryParser:

    BASE_HOST = 'www.lamoda.ru'
    BASE_URL = 'http://' + BASE_HOST
    CATEGORY_URL = 'http://www.lamoda.ru/c/725/clothes-muzhskie-bryuki-klassicheskiye/'

    REQUEST_TIMEOUT = 5

    USE_PROXY = False
    PROXY_LIST_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proxy_list.txt')

    def __init__(self, request=None):
        self._request = request or urllib.request

        if self.USE_PROXY:
            self._init_proxies_from_file()

    def _init_proxies_from_file(self):
        self._proxy_list = [{'http': proxy} for proxy in open(self.PROXY_LIST_FILE_PATH).readlines()]

    def _install_random_proxy(self):
        proxy_handler = urllib.request.ProxyHandler(proxies=random.choice(self._proxy_list))
        proxy_opener = urllib.request.build_opener(proxy_handler)
        self._request.install_opener(proxy_opener)

    def _get_human_headers(self, previous_page_url=None):
        headers = {
            'Host': self.BASE_HOST,
            'Referer': previous_page_url or self.BASE_URL,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'ru',
            'User-Agent': generate_user_agent()
        }

        return headers

    def _make_request_as_human(self, url, params=None, previous_page_url=None):
        if self.USE_PROXY:
            self._install_random_proxy()

        if params:
            url += '?' + urlencode(params)

        human_request = request.Request(url=url, headers=self._get_human_headers(previous_page_url))

        try:
            response = self._request.urlopen(human_request, timeout=self.REQUEST_TIMEOUT)
            gzip_response = gzip.GzipFile(fileobj=response)
            page_html = gzip_response.read()

            return page_html

        except Exception as exception:
            print(exception)

    def get_product_pages_urls(self, page_number=1):
        page = self._make_request_as_human(self.CATEGORY_URL)
        soup = HtmlSoup(page)

        if page_number > 1:
            paginator = soup.find('div', attrs={'class': 'paginator'})
            page_count = int(paginator['data-pages'])

            if page_number > page_count:
                page_number = page_count

            page = self._make_request_as_human(self.CATEGORY_URL, params={'page': page_number})
            soup = HtmlSoup(page)

        product_pages_links = soup.find_all(attrs={'class': 'products-list-item__link'})
        product_urls = [(self.BASE_URL + link['href']) for link in product_pages_links]

        return product_urls

    def get_product(self):
        pass
