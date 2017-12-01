#!/usr/bin/env python

import importlib


BACKEND_MODULES = ('pdfkit', 'trml2pdf')


for module in BACKEND_MODULES:
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        pass
    else:
        importlib.import_module('besserberg.backends._{0}'.format(module))


from besserberg.backends.base import backends_registry  # NOQA
