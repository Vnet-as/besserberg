#!/usr/bin/env python

# std
from io import StringIO, BytesIO
import argparse
# 3p
from PyPDF2 import PdfFileReader, PdfFileWriter
from wand.image import Image
import bottle
import pyqrcode
# project
from besserberg.backends import backends_registry


app = application = bottle.default_app()


def postprocess_pdf(input_pdf, qr_data, qr_x=545, qr_y=20):
    """ PDF post-processor. Append QR code on each PDF page.

    :param input_pdf: PDF byte content
    :param qr_data: QR code data
    :param qr_x: X possition of QR image
    :param qr_y: Y possition of QR image
    """

    qr = pyqrcode.create(qr_data)

    eps = StringIO()
    qr.eps(eps)
    eps.seek(0)

    qr_pdf = BytesIO()

    qr_img = Image(file=BytesIO(bytes(eps.read(), 'utf-8')))
    qr_img.format = 'pdf'
    qr_img.save(qr_pdf)

    qr_page = PdfFileReader(qr_pdf).getPage(0)

    output_writer = PdfFileWriter()
    output_pdf = BytesIO()

    for page in PdfFileReader(BytesIO(input_pdf)).pages:
        page.mergeTranslatedPage(qr_page, qr_x, qr_y)
        output_writer.addPage(page)

    output_writer.write(output_pdf)
    output_pdf.seek(0)

    return output_pdf.read()


@bottle.post('/')
def render_pdf_from_html():
    template = (
        bottle.request.forms.data or bottle.request.forms.template or ''
    )
    backend = bottle.request.forms.backend or 'pdfkit'
    code = bottle.request.forms.qr or None

    print(template)

    try:
        qr_x = int(bottle.request.forms.qr_x or 545)
        qr_y = int(bottle.request.forms.qr_y or 20)
    except ValueError:
        return bottle.HTTPResponse(
            status=400,
            body='Invalid value passed to QR code coordinates.',
        )

    try:
        pdf_file = backends_registry.get(backend).render(template)
    except AttributeError:
        return bottle.HTTPResponse(
            status=400,
            body='Provided backend (%s) is not supported.' % backend,
        )

    if code is not None:
        pdf_file = postprocess_pdf(pdf_file, code, qr_x, qr_y)

    bottle.response.headers['Content-Type'] = 'application/pdf; charset=UTF-8'

    return pdf_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', dest='port', default=8080, type=int)
    parser.add_argument('--host', dest='host', default='0.0.0.0')

    args = parser.parse_args()

    app.run(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
