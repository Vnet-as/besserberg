import pdfkit
from besserberg.backends.base import BesserbergBackend


class PdfKitBackend(BesserbergBackend):

    BACKEND_CODE = 'pdfkit'

    # pdfkit settings 'https://pypi.python.org/pypi/pdfkit'
    OPTIONS = {
        'page-size': 'A4',
        'margin-top': '1cm',
        'margin-right': '1cm',
        'margin-bottom': '1cm',
        'margin-left': '1cm',
        'encoding': "UTF-8",
    }

    def render(self, in_html, options=None):
        return pdfkit.from_string(in_html, False, options=self.OPTIONS)
