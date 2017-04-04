import logging
import json

from urllib import request
from urllib.error import HTTPError
from urllib.parse import urlencode

from settings import YANDEX_API_AUTH_TOKEN


logger = logging.getLogger(__name__)


class YandexMarketAPI:

    API_BASE_URL = 'https://api.content.market.yandex.ru/v1/'

    def __init__(self, token=None):
        self._token = token or YANDEX_API_AUTH_TOKEN

    def _get_api_url(self, resource, formt='json', params=None):
        url = '{}{}.{}'.format(self.API_BASE_URL, resource, formt)
        if params:
            url += '?{}'.format(urlencode(params))
        return url

    def _get_resource(self, resource, params=None, data=None, formt='json'):
        api_url = self._get_api_url(resource, formt, params)
        headers = {
            'Host': 'api.content.market.yandex.ru',
            'Accept': '*/*',
            'Authorization': self._token
        }

        url = request.Request(url=api_url, data=data, headers=headers)

        try:
            response = request.urlopen(url)
            # TODO: XML support
            response_data = response.read()

        except HTTPError as e:
            response_data = e.read()

        return json.loads(response_data.decode('utf-8'))

    def get_categories(self, params):
        if 'geo_id' not in params:
            params['geo_id'] = 213  # Moscow

        return self._get_resource('category', params)
