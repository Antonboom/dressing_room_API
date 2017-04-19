# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


__all__ = (
    'HtmlSoup',
)


class HtmlSoup(BeautifulSoup):

    def insert_before(self, successor):
        pass

    def insert_after(self, successor):
        pass

    def __init__(self, markup, **kwargs):
        if 'features' in kwargs:
            kwargs.pop('features')

        super().__init__(markup, 'html.parser', **kwargs)
