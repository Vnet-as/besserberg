# -*- coding: utf-8 -*-

from besserberg.backends.base import BesserbergBackend

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import trml2pdf


class Trml2PdfBackend(BesserbergBackend):

    BACKEND_CODE = 'trml2pdf'

    RML_FONTS = (
        # (<name>, <path>)
        ('DejaVuSans', 'DejaVuSans.ttf'),
        ('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'),
        ('DejaVuSans-Italic', 'DejaVuSans-Oblique.ttf'),
        ('DejaVuSans-BoldItalic', 'DejaVuSans-BoldOblique.ttf'),
    )

    def __init__(self):

        for font in self.RML_FONTS:
            pdfmetrics.registerFont(TTFont(*font))

    def render(self, template, options=None):
        return trml2pdf.parseString(template)
