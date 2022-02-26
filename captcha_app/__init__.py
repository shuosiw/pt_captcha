# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-20
# @Last Modified by:   Source
# @Last Modified time: 2022-02-26

import os
from flask import Flask
from captcha_app.app import captcha_blue


def create_app():
    app = Flask(__name__)
    app.config['JSON_AS_ASCII'] = False
    app.register_blueprint(captcha_blue) 
    return app
