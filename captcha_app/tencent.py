# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-20
# @Last Modified by:   Source
# @Last Modified time: 2022-02-20

import os
import sys
import base64
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models

class tencent(object):
    """
    tencent cloud ocr class
    """

    def __init__(self, apikey, secret, image, region='ap-guangzhou'):
        cred = credential.Credential(apikey, secret)
        httpProfile = HttpProfile(reqMethod="POST", reqTimeout=60)
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"
        clientProfile.httpProfile = httpProfile
        self.client = ocr_client.OcrClient(cred, region, clientProfile)
        self.image = image


    def get_img_base64(self):
        if not os.path.exists(self.image):
            print 'image file not exists'
            sys.exit(1)
        with open(image, 'rb') as f:
            img_base64 = str(base64.b64encode(f.read()), 'utf-8')
        return img_base64

    def recog_img(self, img_base64):
        params = {"ImageBase64": image}
        req = models.GeneralBasicOCRRequest()
        req.from_json_string(json.dumps(params))
        resp = self.client.GeneralBasicOCR(req)
        for text in resp.TextDetections:
            result = "".join(text.DetectedText)
            result = re.sub(u"([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])", "", result)
        return '"recognition":"' + result + '"'
