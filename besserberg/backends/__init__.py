#!/usr/bin/env python

# std
import importlib
import logging

# project
from besserberg.backends.base import BesserbergBackend


BACKEND_MODULES = ('pdfkit', 'trml2pdf')


for module in BACKEND_MODULES:
    try:
        importlib.import_module(module)
    except ModuleNotFoundError:
        logging.warning(f'module "{module}" not found')
    else:
        importlib.import_module(f'besserberg.backends._{module}')


backends_registry = BesserbergBackend.BACKEND_REGISTRY
