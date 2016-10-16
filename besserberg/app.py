#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyPDF2 import PdfFileReader, PdfFileWriter
from bottle import post, request, response
from io import StringIO, BytesIO
from wand.image import Image

import pyqrcode
import bottle

from besserberg.backends import backends_registry


def postprocess_pdf(input_pdf, qr_data):
    """ PDF post-processor. Append QR code on each PDF page.

    :param input_pdf: pdf byte content
    :param qr_data: :str: QR code data
    """

    qr = pyqrcode.create(qr_data)

    eps = StringIO()
    qr.eps(eps)
    eps.seek(0)

    qr_pdf = BytesIO()

    qr_img = Image(file=BytesIO(bytes(eps.read(), 'utf-8')))
    qr_img.format = "pdf"
    qr_img.save(qr_pdf)

    qr_page = PdfFileReader(qr_pdf).getPage(0)

    output_writer = PdfFileWriter()
    output_pdf = BytesIO()

    for page in PdfFileReader(BytesIO(input_pdf)).pages:
        page.mergeTranslatedPage(qr_page, 545, 20)
        output_writer.addPage(page)

    output_writer.write(output_pdf)
    output_pdf.seek(0)

    return output_pdf.read()


@post('/')
def render_pdf_from_html():

    template = request.body.read().decode("utf-8")
    code = request.query.get('qrcode', None)

    pdf_file = backends_registry.get('pdfkit').render(template)

    if code is not None:
        pdf_file = postprocess_pdf(pdf_file, code)

    response.headers['Content-Type'] = 'application/pdf; charset=UTF-8'

    return pdf_file


def main():
    bottle.run(host='0.0.0.0', port=8080)


if __name__ == '__main__':
    main()
else:
    app = application = bottle.default_app()
