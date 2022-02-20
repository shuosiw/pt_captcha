# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-20
# @Last Modified by:   Source
# @Last Modified time: 2022-02-20

import os
import re
import sys
import base64
import requests

class baidu(object):
    """
    baidu ocr class
    """

    def __init__(self, apikey, secret, image):
        self.image = image
        self.get_token_url = "https://aip.baidubce.com/oauth/2.0/token"
        self.request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        self.params = {
            "grant_type": "client_credentials",
            "client_id": apikey,
            "client_secret": secret,
        }

    def __get_img_base64(self):
        if not os.path.exists(self.image):
            print('image file not exists')
            sys.exit(1)
        with open(self.image, 'rb') as f:
            img_base64 = str(base64.b64encode(f.read()), 'utf-8')
        return img_base64

    def recog_img(self):
        img_base64 = self.__get_img_base64()
        resp = requests.get(self.get_token_url, self.params).json()
        token = resp.get('access_token')
        if not token:
            print('ERROR: cannot get access_token from baidubce')
            sys.exit(1)
        params = {'image': img_base64}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        url = '%(req)s?access_token=%(token)s' % {
            'req': self.request_url,
            'token': token
        }
        ret = requests.post(url, data=params, headers=headers).json()
        """
        ret = { 
            'words_result': [{'words': 'R.5B6B.4'}], 
            'words_result_num': 1, 
            'log_id': 1495362469378575665
        }
        """
        if ret and ret.get('words_result_num') > 0:
            result = "".join(ret['words_result'][0]['words'].split())
            result = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)
            return '"recognition":"%s"' % result
        """
        result = R5B6B4
        """
        else:
            print('ERROR: cannot get recognition from baidubce')
            sys.exit(1)
