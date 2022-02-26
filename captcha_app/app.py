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
from captcha_app.ocr import ocrvd

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
    return ocrvd.current_ocr()

@captcha_blue.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return logout
    imgbase64 = json.loads(request.data).get('image')
    if not imgbase64:
        print('cannot get image base64 data from payload')
        return 'ERROR: image not found!'
    gray_imgbase64 = imgutils(imgbase64).denoise()
    return ocrvd.ocr_output(gray_imgbase64), 200
