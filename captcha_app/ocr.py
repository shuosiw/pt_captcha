# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-23
# @Last Modified by:   Source
# @Last Modified time: 2022-02-26

import os
import sys
import importlib

class ocr(object):
    """docstring for ocr"""
    def __init__(self, vendor, **kwargs):
        self.ocr = getattr(
            importlib.import_module("captcha_app.ocrvendor.%s" % vendor), vendor)
        self.apikey = kwargs.get("apikey")
        self.secret = kwargs.get("secret")
        self.region = kwargs.get("region")
        self.vendor = vendor

    def ocr_output(self, image):
        if image:
            _vendor = self.ocr(apikey=self.apikey,
                 secret=self.secret, region=self.region)
            return _vendor.recog_img(image)
        else:
            print('no image data')
            return

    def current_ocr(self):
        return self.vendor


TX_DEFAULT_REGION = 'ap-guangzhou'

vendor = os.environ.get('OCR_VENDOR')
apikey = os.environ.get('API_KEY')
secret = os.environ.get('SECRET_KEY')
region = os.environ.get('API_REGION')

if not vendor:
    print('please config a vendor with environment variables "OCR_VENDOR"')
    sys.exit(1)
if vendor == 'tencent' and not region:
    print('region not set, use default region: %s' % TX_DEFAULT_REGION)
    region = TX_DEFAULT_REGION
if not apikey or not secret:
    print('apikey or secret not set')
    sys.exit(1)

print('ocr vendor: %s' % vendor)
ocrvd = ocr(vendor, apikey=apikey, secret=secret, region=region)