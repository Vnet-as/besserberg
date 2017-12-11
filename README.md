# Besserberg

## About

besserberg is simple web service for converting HTML or RML files to PDF format. Besides these multiple formats an advantage of the service is ability to append QR code (i.e. invoice number) to each rendered PDF page.

## Run using docker

```shell
$ docker pull vnet/besserberg
$ docker run --rm -p 8000:8000 -t vnet/besserberg python app.py
```

## Usage

```shell
    $ curl -XPOST 'http://localhost:8000' --data 'data=<h1>Hello besserberg!</h1>&backend=pdfkit&qr=secret' > example.pdf
```

## Deployment

If you are running kubernetes check out our kubernetes chart at https://github.com/Vnet-as/charts/tree/master/besserberg
