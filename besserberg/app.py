#!/usr/bin/env python

# std
from io import BytesIO
import argparse
import logging
import os

# 3p
from ppf.datamatrix.datamatrix import DataMatrix
from PyPDF2 import PdfFileReader, PdfFileWriter
from raven import Client
from raven.contrib.bottle import Sentry
from cairosvg import svg2pdf
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


def generate_datamatrix(input_pdf, dm_data, dm_x=545, dm_y=20, scale=1, rectangular=False):
    """
    Generate datamatrix and call pdf for post process
    :param input_pdf: PDF byte content
    :param dm_x: X possition of QR image
    :param dm_y: Y possition of QR image
    :param dm_data: Datamatrix data
    :param scale: scale final image
    :param rectangular: set shape of datamatrix
    """
    dm = DataMatrix(dm_data, rect=rectangular)
    svg = BytesIO(bytes(dm.svg().encode(encoding="utf-8")))
    svg.seek(0)

    return postprocess_pdf(input_pdf, svg, dm_x, dm_y, scale)


def generate_qrcode(input_pdf, qr_data, qr_x=545, qr_y=20, version=None, scale=1, quiet_zone=4):
    """
    Generate Qr code and call pdf for post process
    :param input_pdf: PDF byte content
    :param qr_data: QR code data
    :param qr_x: X possition of QR image
    :param qr_y: Y possition of QR image
    :param version: set QR code density
    :param scale: scale final image
    :param quiet_zone: set QR code corner
    """
    qr = pyqrcode.create(qr_data, version=version, error='Q')

    svg = BytesIO()
    qr.svg(svg, quiet_zone=quiet_zone)
    svg.seek(0)

    return postprocess_pdf(input_pdf, svg, qr_x, qr_y, scale)


def postprocess_pdf(input_pdf, svg, x=545, y=20, scale=1):
    """ PDF post-processor. Append QR code or Datamatrix on each PDF page.

    :param input_pdf: PDF byte content
    :param svg: generated qr code or datametrix in svg format
    :param x: X possition of svg
    :param y: Y possition of svg
    :param scale: set size of final image
    """
    svg_pdf = BytesIO()
    svg2pdf(bytestring=svg.read(), write_to=svg_pdf, background_color="white", scale=scale)
    svg_pdf.seek(0)

    qr_page = PdfFileReader(svg_pdf).getPage(0)

    output_writer = PdfFileWriter()
    output_pdf = BytesIO()

    for page in PdfFileReader(BytesIO(input_pdf)).pages:
        page.mergeTranslatedPage(qr_page, x, y)
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

        scale = 1
        if bottle.request.forms.scale:
            scale = int(bottle.request.forms.scale)

        is_qr = True
        if bottle.request.forms.is_qr:
            if int(bottle.request.forms.is_qr) == 0:
                is_qr = False

        if is_qr:
            version = None
            if bottle.request.forms.version:
                version = int(bottle.request.forms.version)
            quiet_zone = 4
            if bottle.request.forms.quiet_zone:
                quiet_zone = int(bottle.request.forms.quiet_zone)
        else:
            rectangular = False
            if bottle.request.forms.rectangular:
                if int(bottle.request.forms.is_qr) != 0:
                    is_qr = True
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
            if is_qr:
                pdf_file = generate_qrcode(pdf_file, code, qr_x, qr_y, version, scale, quiet_zone)
            else:
                pdf_file = generate_datamatrix(pdf_file, code, qr_x, qr_y, scale, rectangular)
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
