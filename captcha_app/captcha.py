# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-20
# @Last Modified by:   Source
# @Last Modified time: 2022-02-20

import os
import json
import base64
from .imgutils import imgutils
from .baidu import baidu
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
    img_base64 = result['image']
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/upload.png', 'wb') as f:
        f.write(base64.b64decode(img_base64))
    image_in = path + '/upload.png'
    image_out = path + '/code.png'
    imgut = imgutils(image_in, image_out)
    imgut.denoise()
    bd = baidu(current_app.config['API_KEY'], current_app.config['SECRET_KEY'], image_out)
    return bd.recog_img(), 200
