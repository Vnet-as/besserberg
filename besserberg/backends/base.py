#!/usr/bin/env python


class BesserbergBackend:
    '''
    Base class for all besserberg's PDF backends.
    '''

    BACKEND_CODE = None
    BACKEND_REGISTRY = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.BACKEND_CODE in cls.BACKEND_REGISTRY:
            raise KeyError(f'{cls.BACKEND_CODE} already exists')
        cls.BACKEND_REGISTRY[cls.BACKEND_CODE] = cls()

    @classmethod
    def get_code(cls):
        return cls.BACKEND_CODE

    def render(self, template, options=None):
        raise NotImplementedError('Subclass must implement this method')
