#!/usr/bin/env python

# 3p
import pdfkit
# project
from besserberg.backends.base import BesserbergBackend


class PdfKitBackend(BesserbergBackend):

    BACKEND_CODE = 'pdfkit'

    # pdfkit settings 'https://pypi.python.org/pypi/pdfkit'
    OPTIONS = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
        'no-outline': None,
    }

    # filter for options passed to render method
    _allowed_options = [
        'footer-left', 'footer-right', 'footer-center',
        'header-left', 'header-right', 'header-center',
    ]

    def render(self, template, options=None):
        options = {
            k: options[k]
            for k in self._allowed_options if k in options
        } if isinstance(options, dict) else {}

        options.update(self.OPTIONS)

        return pdfkit.from_string(template, False, options=options)
