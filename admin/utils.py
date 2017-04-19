# -*- coding: utf-8 -*-


def ellipsis(text, limit=50):
    """
    :type text: str
    """

    if len(text) < limit:
        return text

    return text[:limit - 3] + '...'
