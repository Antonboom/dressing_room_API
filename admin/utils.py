# -*- coding: utf-8 -*-

import hashlib
from urllib.parse import urljoin

from werkzeug.utils import secure_filename

import settings


def ellipsis(text, limit=50):
    """
    :type text: str
    """

    if len(text) < limit:
        return text

    return text[:limit - 3] + '...'


def get_photo_filename(obj, file_data):
    return hashlib.sha256(secure_filename(file_data.filename).encode('utf-8')).hexdigest()


def get_photo_thumbname(filename):
    return filename
