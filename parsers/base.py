# -*- coding: utf-8 -*-

import traceback
import os
import random
import gzip
import time
import urllib

from urllib import request
from urllib.parse import urlencode, urlparse
from user_agent import generate_user_agent

from application import db
from parsers.utils import HtmlSoup

"""
Proxy sources:
    https://hidemy.name/en/proxy-list/?maxtime=1500&type=h&anon=3#list
    http://proxyserverlist-24.blogspot.ru
"""


__all__ = (
    'MarketPlaceCategoryParser',
)


class MarketPlaceCategoryParser:

    REQUEST_TIMEOUT = 5

    SLEEP_PER_REQUEST = 1

    USE_PROXY = False
    PROXY_LIST_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'proxy_list.txt')

    def __init__(self, source, category, request=None):
        """
        :type category: models.Category
        """

        self._request = request or urllib.request

        if self.USE_PROXY:
            self._init_proxies_from_file()

        self.category = category

        self.source = source
        self._base_url = source.site_url
        self._base_host = urlparse(source.site_url).hostname

    def _init_proxies_from_file(self):
        self._proxy_list = [{'http': proxy} for proxy in open(self.PROXY_LIST_FILE_PATH).readlines()]

    def _install_random_proxy(self):
        proxy_handler = urllib.request.ProxyHandler(proxies=random.choice(self._proxy_list))
        proxy_opener = urllib.request.build_opener(proxy_handler)
        self._request.install_opener(proxy_opener)

    def _get_human_headers(self, previous_page_url=None):
        headers = {
            'Host': self._base_host,
            'Referer': previous_page_url or self._base_url,
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

        response = self._request.urlopen(human_request, timeout=self.REQUEST_TIMEOUT)
        gzip_response = gzip.GzipFile(fileobj=response)
        page_html = gzip_response.read()

        return page_html

    def get_product_pages_urls(self, page_number=1):
        raise NotImplementedError

    def get_product(self, product_page_soup):
        raise NotImplementedError

    def get_products(self, pages_count=1):
        products = []

        for page in range(1, pages_count + 1):
            product_urls = self.get_product_pages_urls(page)

            for product_url in product_urls[:1]:
                print(product_url)

                page = self._make_request_as_human(product_url)
                soup = HtmlSoup(page)

                product = None
                try:
                    product = self.get_product(soup)

                except Exception as exception:
                    print('Received error: ', exception, traceback.format_exc())

                if not product:
                    continue

                product.url = product_url
                products.append(product)

                time.sleep(self.SLEEP_PER_REQUEST)

        return products
