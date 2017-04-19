# -*- coding: utf-8 -*-

from urllib.parse import urljoin

from models import Product, Color
from parsers.base import MarketPlaceCategoryParser
from parsers.utils import HtmlSoup


class LamodaCategoryParser(MarketPlaceCategoryParser):

    @staticmethod
    def _only_digits(text):
        return ''.join([symbol for symbol in text if symbol.isdigit()])

    @staticmethod
    def _only_alphas(text):
        return ''.join([symbol for symbol in text if symbol.isalpha()])

    # 'lamoda attribute name': (canonize_func, product_field)
    PRODUCT_ATTRIBUTES_MAP = {
        'Высота':                   (_only_digits, 'height'),
        'Длина':                    (_only_digits, 'length'),
        'Длина по внутреннему шву': (_only_digits, 'inner_seam_length'),
        'Длина по боковому шву':    (_only_digits, 'along_side_seam_length'),
        'Обхват по талии':          (_only_digits, 'circumference_at_waist'),
        'Обхват по бедрам':         (_only_digits, 'circumference_at_hips'),
        'Ширина по низу':           (_only_digits, 'bottom_width'),
        'Цвет':                     (_only_alphas, 'color')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not self.category.lamoda_url:
            raise AttributeError('Please set lamoda_url for {}'.format(self.category))

    def get_product_pages_urls(self, page_number=1):
        category_url = self.category.lamoda_url

        page = self._make_request_as_human(category_url)
        soup = HtmlSoup(page)

        if page_number > 1:
            paginator = soup.find('div', attrs={'class': 'paginator'})
            page_count = int(paginator['data-pages'])

            if page_number > page_count:
                return []

            page = self._make_request_as_human(category_url, params={'page': page_number})
            soup = HtmlSoup(page)

        product_pages_links = soup.find_all(attrs={'class': 'products-list-item__link'})
        product_urls = [urljoin(self._base_url, link['href']) for link in product_pages_links]

        return product_urls

    def _get_product_name(self, product_page_soup):
        """
        :type product_page_soup: lamoda_parser.utils.HtmlSoup
        """

        name = product_page_soup.find('h1', attrs={'class': 'ii-product__title'}).string

        return name

    def _get_product_photo_url(self, product_page_soup):
        """
        :type product_page_soup: lamoda_parser.utils.HtmlSoup
        """

        photo = product_page_soup.find('img', attrs={'class': 'showcase__item-image'})
        photo_url = photo['src']

        if photo_url.startswith('//'):
            photo_url = 'http:' + photo_url

        return photo_url

    def _get_product_price(self, product_page_soup):
        """
        :type product_page_soup: lamoda_parser.utils.HtmlSoup
        """

        price = product_page_soup.find('div', attrs={'class': 'ii-product__price-current'})
        price_value = int(self._only_digits(price.string))

        return price_value

    def _get_product_attributes(self, product_page_soup):
        """
        :type product_page_soup: lamoda_parser.utils.HtmlSoup
        """

        lamoda_attributes = product_page_soup.find_all('div', attrs={'class': 'ii-product__attribute'})

        lamoda_attributes_dict = {
            attribute.find('span', attrs={'class': 'ii-product__attribute-label'}).string:
            attribute.find('span', attrs={'class': 'ii-product__attribute-value'}).string
            for attribute in lamoda_attributes
        }

        # TODO: Terrible code!
        product_attributes = {
            self.PRODUCT_ATTRIBUTES_MAP[lamoda_attr][1]: self.PRODUCT_ATTRIBUTES_MAP[lamoda_attr][0].__func__(lamoda_attr_value)
            for lamoda_attr, lamoda_attr_value in lamoda_attributes_dict.items()
            if lamoda_attr in self.PRODUCT_ATTRIBUTES_MAP
        }

        description = product_page_soup.find('span', attrs={'itemprop':'description'}).string.strip()
        product_attributes['description'] = description

        return dict(product_attributes)

    def get_product(self, product_page_soup):
        """
        :type product_page_soup: lamoda_parser.utils.HtmlSoup
        """

        name = self._get_product_name(product_page_soup)
        photo_url = self._get_product_photo_url(product_page_soup)
        price = self._get_product_price(product_page_soup)

        product_data = self._get_product_attributes(product_page_soup)

        product_data.update({
            'name': name,
            'price': price,
            'gender': self.category.gender,
            'is_childish': self.category.is_childish,
            'category_id': self.category.id,
            'source_id': self.source.id
        })

        product = Product(**product_data)

        color = Color.query.filter_by(name=product_data.get('color')).first()
        if color:
            product.colors.append(color)

        product.set_photo(photo_url)

        return product
