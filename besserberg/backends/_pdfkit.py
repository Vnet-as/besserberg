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
    }

    def render(self, template, options=None):
        return pdfkit.from_string(template, False, options=self.OPTIONS)
