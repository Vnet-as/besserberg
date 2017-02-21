# -*- coding: utf-8 -*-

from besserberg.backends.base import BesserbergBackend

import trml2pdf


class Trml2PdfBackend(BesserbergBackend):

    BACKEND_CODE = 'trml2pdf'

    def render(self, template, options=None):
        return trml2pdf.parseString(template)
