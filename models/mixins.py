# -*- coding: utf-8 -*-

from application import db


__all__ = (
    'SetFieldsMixin'
)


class RequiredFieldError(Exception):
    pass


class SetFieldsMixin:

    required_fields = ()
    not_required_fields = ()

    def __init__(self, *args, **kwargs):
        try:
            [setattr(self, field, kwargs[field]) for field in self.required_fields]
            [setattr(self, field, kwargs[field]) for field in self.not_required_fields if field in kwargs]

        except KeyError as exception:
            raise RequiredFieldError(
                'Field "{}" is required for "{}" model'.format(exception.args[0], self.__class__.__name__))

        super().__init__(*args, **kwargs)

    def serialize(self):
        fields = self.required_fields + self.not_required_fields
        return {field: getattr(self, field) for field in fields if getattr(self, field)}
