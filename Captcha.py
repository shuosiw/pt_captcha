#!/usr/bin/env python
# -*- coding:utf-8 -*-
############################################################
# @Author       : Sean
# @Date         : 2022-01-11 14:43:36
# @LastEditors  : Sean
# @LastEditTime : 2022-01-25 16:34:57
# @Description  : 这是由 Sean 创建
# @FilePath     : d:/我的文件/0-项目/Python/验证码识别/Captcha.py
# @Copyright    : Copyright ©2019-2022 Sean,Inc
############################################################

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
from flask import Flask, request
from PIL import Image
import requests
import base64
import json
import os
import re

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
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
    </html>'''
# #忽略的检查的url
# NOT_CHECK_URL=['/']

# @app.before_request
# def login_required():
#     if request.path not in NOT_CHECK_URL:


@app.route('/', methods=['GET'])
def index():
    return logout


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return logout
    result = json.loads(request.data)
    api = result['api']
    id = result['id']
    secret = result['secret']
    region = result['region']
    img_base64 = result['image']
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/upload.png', 'wb') as f:
        f.write(base64.b64decode(img_base64))
    image_up = path + '/upload.png'
    image_out = path + '/code.png'
    # 图片进行灰度处理
    image = Image.open(image_up)
    imgry = image.convert('L')
    # 获取灰度转二值的映射table,0表示黑色,1表示白色
    threshold = 115
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    binary = imgry.point(table, '1')

    def sum_9_region_new(img, x, y):
        '''确定噪点'''
        cur_pixel = img.getpixel((x, y))  # 当前像素点的值
        width = img.width
        height = img.height
        if cur_pixel == 1:  # 如果当前点为白色区域,则不统计邻域值
            return 0
        # 因当前图片的四周都有黑点，所以周围的黑点可以去除
        if y < 3:  # 本例中，前两行的黑点都可以去除
            return 1
        elif y > height - 3:  # 最下面两行
            return 1
        else:  # y不在边界
            if x < 3:  # 前两列
                return 1
            elif x == width - 1:  # 右边非顶点
                return 1
            else:  # 具备9领域条件的
                sum = img.getpixel((x - 1, y - 1)) \
                    + img.getpixel((x - 1, y)) \
                    + img.getpixel((x - 1, y + 1)) \
                    + img.getpixel((x, y - 1)) \
                    + cur_pixel \
                    + img.getpixel((x, y + 1)) \
                    + img.getpixel((x + 1, y - 1)) \
                    + img.getpixel((x + 1, y)) \
                    + img.getpixel((x + 1, y + 1))
                return 9 - sum

    def collect_noise_point(img):
        '''收集所有的噪点'''
        noise_point_list = []
        for x in range(img.width):
            for y in range(img.height):
                res_9 = sum_9_region_new(img, x, y)
                if (0 < res_9 < 3) and img.getpixel((x, y)) == 0:  # 找到孤立点
                    pos = (x, y)
                    noise_point_list.append(pos)
        return noise_point_list

    def remove_noise_pixel(img, noise_point_list):
        '''根据噪点的位置信息，消除二值图片的黑点噪声'''
        for item in noise_point_list:
            img.putpixel((item[0], item[1]), 1)

    def get_result_tx(id, secret, region, image):
        '''腾讯验证码识别函数'''
        try:
            cred = credential.Credential(id, secret)
            httpProfile = HttpProfile(reqMethod="POST", reqTimeout=60)
            httpProfile.endpoint = "ocr.tencentcloudapi.com"

            clientProfile = ClientProfile()
            clientProfile.signMethod = "TC3-HMAC-SHA256"
            clientProfile.httpProfile = httpProfile
            client = ocr_client.OcrClient(cred, region, clientProfile)
            with open(image, 'rb') as f:
                image = str(base64.b64encode(f.read()), 'utf-8')
            req = models.GeneralBasicOCRRequest()
            params = {"ImageBase64": image}
            req.from_json_string(json.dumps(params))
            resp = client.GeneralBasicOCR(req)
            for text in resp.TextDetections:
                result = "".join(text.DetectedText)
                result = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)
            return '"recognition":"' + result + '"'
        except TencentCloudSDKException as err:
            return err

    def get_result_bd(id, secret, image):
        '''百度验证码识别函数'''
        get_token_url = "https://aip.baidubce.com/oauth/2.0/token"
        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        params = {
            "grant_type": "client_credentials",
            "client_id": id,
            "client_secret": secret,
        }
        response = requests.get(get_token_url, params).json()
        token = response['access_token']
        with open(image, 'rb') as f:
            image = base64.b64encode(f.read())
        params = {'image': image}
        access_token = token
        request_url = request_url + '?access_token=' + access_token
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        response = requests.post(request_url, data=params, headers=headers).json()
        if response:
            result = response['words_result'][0]['words'].split()
            result = "".join(result)
            result = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)
            return '"recognition":"' + result + '"'

    noise_point_list = collect_noise_point(binary)
    remove_noise_pixel(binary, noise_point_list)
    binary.save(image_out)
    if 'bd' == api:
        return get_result_bd(id, secret, image_out), 200
    elif 'tx' == api:
        if region == "":
            return get_result_tx(id, secret, "ap-shanghai", image_out), 200
        else:
            return get_result_tx(id, secret, region, image_out), 200
    else:
        return get_result_bd(id, secret, image_out), 200


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)