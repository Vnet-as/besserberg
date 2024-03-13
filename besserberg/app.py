#!/usr/bin/env python

# std
from io import StringIO, BytesIO
import argparse
import logging
import os

# 3p
from PyPDF2 import PdfFileReader, PdfFileWriter
from raven import Client
from raven.contrib.bottle import Sentry
from wand.image import Image
import bottle
import pyqrcode

# project
from besserberg.backends import backends_registry


# update bottle's max payload size due to large templates
bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024
# create logger
logger = logging.getLogger(__name__)
# initialize bottle application
app = application = bottle.default_app()
app.catchall = False
# initialize sentry and use one as wrapper for bottle application
sentry_client = Client(os.environ.get('SENTRY_DSN'), auto_log_stacks=True)
app = Sentry(app, sentry_client)


def postprocess_pdf(input_pdf, qr_data, qr_x=545, qr_y=20, version=None, scale=1, quiet_zone=4):
    """ PDF post-processor. Append QR code on each PDF page.

    :param input_pdf: PDF byte content
    :param qr_data: QR code data
    :param qr_x: X possition of QR image
    :param qr_y: Y possition of QR image
    :param version: set QR code density
    :param scale: set size of final image
    :param quiet_zone: set QR code corner
    """

    qr = pyqrcode.create(qr_data, version=version)

    png = BytesIO()
    qr.png(png, scale=scale, quiet_zone=quiet_zone)
    png.seek(0)
    
    qr_pdf = BytesIO()

    qr_img = Image(file=png)
    qr_img.format = 'pdf'
    qr_img.save(qr_pdf)
    qr_pdf.seek(0)

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
    options = bottle.request.forms.decode()

    try:
        qr_x = int(bottle.request.forms.qr_x or 545)
        qr_y = int(bottle.request.forms.qr_y or 20)
        version = None
        if bottle.request.forms.version:
            version = int(bottle.request.forms.version)
        scale = 1
        if bottle.request.forms.scale:
            scale = int(bottle.request.forms.scale)
        quiet_zone = 4
        if bottle.request.forms.quiet_zone:
            quiet_zone = int(bottle.request.forms.quiet_zone)
    except ValueError:
        return bottle.HTTPResponse(
            status=400,
            body='Invalid value passed to QR code coordinates.',
        )

    try:
        pdf_file = backends_registry.get(backend).render(template, options)
    except AttributeError:
        return bottle.HTTPResponse(
            status=400,
            body='Provided backend (%s) is not supported.' % backend,
        )

    if code is not None:
        try:
            pdf_file = postprocess_pdf(pdf_file, code, qr_x, qr_y, version, scale, quiet_zone)
        except ValueError:
            logger.error('Failed to append QR code', exc_info=True)
            return bottle.HTTPResponse(
                status=422,
                body='Unable to append QR code to rendered template.',
            )

    bottle.response.headers['Content-Type'] = 'application/pdf; charset=UTF-8'

    return pdf_file


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', dest='port', default=8080, type=int)
    parser.add_argument('--host', dest='host', default='0.0.0.0')
    parser.add_argument('--sentry-dsn', dest='sentry_dsn', default=None)
    args = parser.parse_args()

    if args.sentry_dsn is not None:
        sentry_client.set_dsn(args.sentry_dsn)

    bottle.run(app=app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()
