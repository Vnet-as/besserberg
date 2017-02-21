==========
Besserberg
==========

About
~~~~~

besserberg is simple web service for converting HTML or RML files to PDF format. Besides these multiple formats an advantage of the service is ability to append QR code (i.e. invoice number) to each rendered PDF page.

Running
~~~~~~~

::

    $ docker pull vnet/besserberg
    $ docker run --rm -p 8080:8080 -t vnet/besserberg python app.py

Usage example
~~~~~~~~~~~~~

::

    curl -XPOST 'http://localhost:8080' --data 'body="<h1>Hello besserberg!</h1>"&backend=pdfkit&qr=secret' > hello.pdf

Deployment
~~~~~~~~~~

If you are running kubernetes check out our kubernetes chart at https://github.com/Vnet-as/charts/tree/master/besserberg


Otherwise you can use our docker image with built-in uwsgi server:

::

    $ docker pull vnet/besserberg
    $ docker run -d --name besserberg_wsgi -t vnet/besserberg
