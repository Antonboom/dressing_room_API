# -*- coding: utf-8 -*-

import json

from flask import Response


__all__ = (
    'JsonResponse',
)


class JsonResponse(Response):

    def __init__(self, response, *agrs, **kwargs):
        super().__init__(
            json.dumps(response, ensure_ascii=False, indent=4, sort_keys=True),
            *agrs,
            content_type='application/json;charset=utf-8',
            **kwargs
        )
