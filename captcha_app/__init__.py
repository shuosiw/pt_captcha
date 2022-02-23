# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-20
# @Last Modified by:   Source
# @Last Modified time: 2022-02-23

import os
from flask import Flask
from .captcha import captcha_blue


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['OCR_VENDOR'] = os.environ.get('OCR_VENDOR', 'null')
    app.config['API_KEY'] = os.environ.get('API_KEY', 'null')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'null')
    app.config['API_REGION'] = os.environ.get('API_REGION', 'null')
    app.register_blueprint(captcha_blue) 
    return app
