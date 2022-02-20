# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-20
# @Last Modified by:   Source
# @Last Modified time: 2022-02-20

import os
from flask import Flask
from .captcha import captcha_blue


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.config['API_TYPE'] = os.environ.get('API_TYPE', 'null')
    app.config['API_KEY'] = os.environ.get('API_KEY', 'null')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'null')
    app.config['TX_REGION'] = os.environ.get('TX_REGION', 'null')
    app.register_blueprint(captcha_blue) 
    return app
