# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-23
# @Last Modified by:   Source
# @Last Modified time: 2022-02-23

import sys
import importlib

class ocr(object):
    """docstring for ocr"""
    def __init__(self, vendor, **kwargs):
        self.vendor = getattr(
            importlib.import_module("captcha_app.ocrvendor.%s" % vendor), vendor)
        self.apikey = kwargs.get("apikey")
        self.secret = kwargs.get("secret")
        self.image = kwargs.get("image")
        self.region = kwargs.get("region")

    def ocr_output(self):
        if all([self.apikey, self.secret, self.image]):
            _vendor = self.vendor(apikey=self.apikey,
                 secret=self.secret, image=self.image, region=self.region)
            return _vendor.recog_img()
