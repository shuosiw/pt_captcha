# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-20
# @Last Modified by:   Source
# @Last Modified time: 2022-02-26

import os
import json
import base64
from flask import request, Blueprint, current_app
from captcha_app.utils import imgutils
from captcha_app.ocr import ocr


captcha_blue = Blueprint('routes', __name__)

vendor = os.environ.get('OCR_VENDOR', 'null')
apikey = os.environ.get('API_KEY', 'null')
secret = os.environ.get('SECRET_KEY', 'null')
region = os.environ.get('API_REGION', 'null')
ocrvd = ocr(vendor, apikey=apikey, secret=secret, region=region)


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
    return ocrvd.ocr_output(gray_imgbase64), 200
