# ASN (Archive Serial Number) Cover Page Remover

The purpose of this script is to remove pages from a PDF document
that contain QR Codes with data in the format of ASNXXXXXXX.

This script is meant to be used as a [pre-consuption script for paperless-ngx](https://docs.paperless-ngx.com/advanced_usage/#pre-consume-script)

## Why
There are some documents that I did not want to add a sticker to, but still keep physical copies.
In order to automatically assign an ASN in paperless, I create ASN cover pages using [asn-pdf-generator](https://github.com/cmilam87/asn-pdf-generator). However, I did not want
this cover page to be a part of the digital document in paperless-ngx.

## Setup
Run the following commands on the machine (virtual or otherwise) that is hosting paperless-ngx
1. Create a folder to save the scripts and virtual environment `mkdir scripts`
2. cd into scripts directory `cd scripts`
3. Create a virtual environment `python -m venv venv`
4. Activate the virtual environment using one of the commands below
```
source venv/bin/activate
. venv/bin/activate` #remember the dot!
```
5. Install the dependencies `pip install PyPDF2 pyzbar Pillow`
6. Copy `remove-asn-cover-page.sh` and `remove-asn-cover-page.py` to the `scripts` directory

## Paperless Configuration
1. Set the `PAPERLESS_PRE_CONSUME_SCRIPT` to the full path of the bash script. This must be the full path including the script name. Example: `/mnt/scripts/remove-asn-cover-page.sh`
2. Set `PAPERLESS_CONSUMER_ENABLE_BARCODES` to true
3. Set `PAPERLESS_CONSUMER_ENABLE_ASN_BARCODE` to true