#!/usr/bin/env python

# 3p
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import trml2pdf
# project
from besserberg.backends.base import BesserbergBackend


class Trml2PdfBackend(BesserbergBackend):

    BACKEND_CODE = 'trml2pdf'

    RML_FONTS = (
        ('DejaVuSans', 'DejaVuSans.ttf'),
        ('DejaVuSans-Bold', 'DejaVuSans-Bold.ttf'),
        ('DejaVuSans-Italic', 'DejaVuSans-Oblique.ttf'),
        ('DejaVuSans-BoldItalic', 'DejaVuSans-BoldOblique.ttf'),
        ('DejaVuSansCondensed', 'DejaVuSansCondensed.ttf'),
        ('DejaVuSansCondensed-Bold', 'DejaVuSansCondensed-Bold.ttf'),
        ('DejaVuSansCondensed-Italic', 'DejaVuSansCondensed-Oblique.ttf'),
        ('DejaVuSansCondensed-BoldItalic', 'DejaVuSansCondensed-BoldOblique.ttf'),
    )

    RML_FONT_FAMILIES = {
        'DejaVuSans': {
            'normal': 'DejaVuSans',
            'bold': 'DejaVuSans-Bold',
            'italic': 'DejaVuSans-Italic',
            'boldItalic': 'DejaVuSans-BoldItalic',
        },
        'DejaVuSansCondensed': {
            'normal': 'DejaVuSansCondensed',
            'bold': 'DejaVuSansCondensed-Bold',
            'italic': 'DejaVuSansCondensed-Italic',
            'boldItalic': 'DejaVuSansCondensed-BoldItalic',
        }
    }

    def __init__(self):
        for font in self.RML_FONTS:
            pdfmetrics.registerFont(TTFont(*font))

        for family_name, family_fonts in self.RML_FONT_FAMILIES.items():
            pdfmetrics.registerFontFamily(family_name, **family_fonts)

    def render(self, template, options=None):
        return trml2pdf.parseString(template)
