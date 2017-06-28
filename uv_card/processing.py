# -*- coding: utf-8 -*-

import os

from wand.image import Image


class UVcardPart:

    def __init__(self, image_filepath, width, height, left, top):
        self._image = Image(filename=image_filepath)

        self._width = width
        self._height = height
        self._top = top
        self._left = left

        self._crop_image()

    def _crop_image(self):
        self._image.crop(left=self._left, top=self._top, width=self._width, height=self._height)

    @property
    def image(self):
        return self._image

    @property
    def position(self):
        return self._left, self._top

    @property
    def left(self):
        return self._left

    @property
    def top(self):
        return self._top


class UVcard:

    WIDTH = 1024
    HEIGHT = 1024

    BACKGROUND_PATH = os.path.join(os.path.dirname(__file__), 'static', 'images', 'default_uvcard.jpg')

    def __init__(self, *parts, **kwargs):
        """
        :type parts: list[UVcardPart]
        """

        self._background_image = Image(filename=self.BACKGROUND_PATH)
        self._width = kwargs.get('width', self.WIDTH)
        self._height = kwargs.get('height', self.HEIGHT)
        self._parts = parts

        self._composite()

    def _composite(self):
        for part in self._parts:
            if not isinstance(part, UVcardPart):
                raise ValueError('Image part should be instance of <class "UVcardPath">')
            self._background_image.composite(part.image, *part.position)

    def make_blob(self):
        return self._background_image.make_blob('jpeg')
