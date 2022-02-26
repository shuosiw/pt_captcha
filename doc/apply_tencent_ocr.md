## 申请腾讯云 OCR 接入

> 其他问题参考：[文字识别接入常见问题](https://cloud.tencent.com/developer/article/1700555)

1. 注册账号（第一次登录需要关联微信账号）：[https://cloud.tencent.com/](https://cloud.tencent.com/)

![image.png](https://cdn.nlark.com/yuque/0/2022/png/21616917/1645864894129-4096ff80-8016-4087-a727-c95d4093aa32.png#clientId=ua75f569e-736b-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=245&id=u3a7b4b7f&margin=%5Bobject%20Object%5D&name=image.png&originHeight=489&originWidth=524&originalType=binary&ratio=1&rotation=0&showTitle=false&size=106948&status=done&style=none&taskId=u96cb895b-b606-46a7-9c06-c1a954b7647&title=&width=262)

2. 开通 OCR 服务：[https://console.cloud.tencent.com/ocr/general](https://console.cloud.tencent.com/ocr/general)

![image.png](https://cdn.nlark.com/yuque/0/2022/png/21616917/1645864990108-fe594bf6-395f-41f6-87d9-0e0f8a3ba0e8.png#clientId=ua75f569e-736b-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=237&id=uca530b66&margin=%5Bobject%20Object%5D&name=image.png&originHeight=490&originWidth=984&originalType=binary&ratio=1&rotation=0&showTitle=false&size=55127&status=done&style=none&taskId=ubd1b1e51-4d18-4ef9-9b4f-f37e93239b4&title=&width=476)

3. 申请访问密钥（推荐创建子用户只分配 ocr 权限）：[https://console.cloud.tencent.com/cam/capi](https://console.cloud.tencent.com/cam/capi)

![image.png](https://cdn.nlark.com/yuque/0/2022/png/21616917/1645865267618-64120899-4efd-4036-8699-2d13684dba04.png#clientId=ua75f569e-736b-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=179&id=u42804cc6&margin=%5Bobject%20Object%5D&name=image.png&originHeight=358&originWidth=968&originalType=binary&ratio=1&rotation=0&showTitle=false&size=21706&status=done&style=none&taskId=u7d7c4d28-e59a-454c-83dd-764850e6a50&title=&width=484)
需要注意，腾讯的免费额度不是立即分配的，通常是在整点分配，所以如果创建好账号后调用出现如下报错：
```python
[TencentCloudSDKException] code:ResourcesSoldOut.ChargeStatusException message:计费状态异常 
```
可能是免费额度未更新，需要再等待一段时间（过了整点）再尝试

