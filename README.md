## README

### 说明

针对 pt 站点常用的验证码进行预处理并调用腾讯/百度的 ocr api 进行识别，通常用于自动签到

大致的使用流程如下：

1. 首先需要开通百度或腾讯任意一个 ocr 服务，获取到 apikey 及 secret
2. 通过设置环境变量的方式进行配置，并启动运行服务（建议使用 docker 运行）
3. 通过 http 接口调用 POST base64 编码的图片数据，接口将响应并返回识别结果

### 使用

#### 申请凭证

首先需要选择一个 ocr 服务提供方申请接入，并拿到 apikey 及 secret 凭证，具体参考：

* [申请百度智能云 OCR 接入](https://github.com/shuosiw/pt_captcha/doc/apply_baidu_ocr.md)
* [申请腾讯云 OCR 接入](https://github.com/shuosiw/pt_captcha/doc/apply_tencent_ocr.md)




#### 启动服务

以腾讯云为例，假设已经获取到的凭证已经保存到对应变量：

* apikey: `$TENCENT_SECRET_ID`
* secret: `$TENCENT_SECRET_KEY`

则容器启动命令如下：

```
docker run -d --rm -p 5000:5000 \
    -e API_KEY="$TENCENT_SECRET_ID"\
    -e SECRET_KEY="$TENCENT_SECRET_KEY" \
    -e OCR_VENDOR='tencent' shuosiw/pt_captcha:latest
```

之后就可以通过容器宿主的 `5000` 端口访问

![unraid](https://github.com/shuosiw/pt_captcha/raw/master/images/unraid.png)

假设你使用的是 unraid，**强烈推荐使用我提供的 unraid docker模板库来安装**，详细使用方式见：
* https://github.com/shuosiw/unraid


#### 服务测试

假设容器宿主 IP 为 `10.0.0.100`，则可通过以下方式来查看当前使用的哪个服务提供商：

```
curl http://10.0.0.100:5000/current_ocr
```

因为上文中使用了腾讯的服务，所以该命令会返回 `tencent`

#### 图片识别

首先我们需要将验证码图片转为 base64 编码，本仓库 `image` 目录下提供的示例图片为例：

![captcha](https://github.com/shuosiw/pt_captcha/raw/master/images/example.png)

将其通过代码或者在线网站转成 base64 编码，假设将其赋值到变量 `$IMAGE_BASE64`，然后就可通过 POST 方法调用该接口进行识别，具体方式如下：

```
curl -X POST http://10.0.0.100:5000/upload \
    -H 'Content-Type: text/json' \
    -d "{'image': '$IMAGE_BASE64'}"
```

最终返回数据为：

```
"recognition":"R5B6B4"
```

### 参数

本仓库只提供容器运行方案，对应配置均通过环境变量进行设置：

|变量名|是否必须|说明|
|---|---|---|
| `OCR_VENDOR` | 是 | 目前仅支持 `tencent` 与 `baidu` |
| `API_KEY` | 是 | 认证凭证，对应关系见下方 |
| `SECRET_KEY` |是|认证凭证，对应关系见下方 |
| `API_REGION` | 否 | 调用 api 所在 region，默认使用 `ap-guangzhou` |


各厂商对应 `API_KEY` 与 `SECRET_KEY` 叫法如下：

|提供方| apikey | secret |
|---|---|---|
| 百度 | `API Key` | `Secret Key` |
| 腾讯 | `SecretId` | `SecretKey` |


另外，`API_REGION` 仅在使用腾讯 ocr 接口时有效，其可选值为：

|地域|    取值|
|---|---|
|华北地区(北京)   | `ap-beijing` |
|华南地区(广州)   | `ap-guangzhou` |
|华东地区(上海)   | `ap-shanghai` |
|港澳台地区(中国香港)    | `ap-hongkong` |
|北美地区(多伦多)  | `na-toronto` |


### 感谢

* https://registry.hub.docker.com/r/sean0/pt_captcha