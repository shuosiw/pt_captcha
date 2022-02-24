# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-20
# @Last Modified by:   Source
# @Last Modified time: 2022-02-25

import os
import json
import base64
from .imgutils import imgutils
from .ocr import ocr
from flask import request, Blueprint, current_app

captcha_blue = Blueprint('routes', __name__)


logout = '''
    <html>
    <body onload='setTimeout("mm()",100000)'>
    <script>
    function mm()
    {
        window.opener=null;
        window.close();
    }
    </script>
    </body>
    </html>
'''

@captcha_blue.route('/', methods=['GET'])
def index():
    return logout

@captcha_blue.route('/current_ocr', methods=['GET'])
def current_ocr():
    return current_app.config['API_TYPE']

@captcha_blue.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return logout
    result = json.loads(request.data)
    imgbase64 = result.get('image')
    if not imgbase64:
        print('cannot get image base64 data from payload')
        return 'ERROR: image not found!'
    gray_imgbase64 = imgutils(imgbase64).denoise()
    vendor = ocr(vendor=current_app.config['OCR_VENDOR'],
        apikey=current_app.config['API_KEY'], secret=current_app.config['SECRET_KEY'],
        region=current_app.config['API_REGION'])
    return vendor.ocr_output(gray_imgbase64), 200
