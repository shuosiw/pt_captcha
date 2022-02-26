# -*- coding: utf-8 -*-
# @Author: Source
# @Date:   2022-02-20
# @Last Modified by:   Source
# @Last Modified time: 2022-02-24

import base64
from io import BytesIO
from PIL import Image

class imgutils(object):
    """
    utils for image pre-process
    """

    def __init__(self, imgbase64, threshold=115):
        self.imgbase64 = imgbase64
        self.threshold = threshold

    def grayscale(self):
        """
        transfer to Grayscale processing
        """
        img = Image.open(BytesIO(base64.b64decode(self.imgbase64)))
        imgry = img.convert('L')
        threshold = self.threshold
        table = []
        for i in range(256):
            if i < threshold:
                table.append(0)
            else:
                table.append(1)
        imgbin = imgry.point(table, '1')
        return imgbin

    def __sum_9_region_new(self, imgbin, x, y):
        """
        detect noise point
        """
        cur_pixel = imgbin.getpixel((x, y))  # 当前像素点的值
        width = imgbin.width
        height = imgbin.height
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
                sum = imgbin.getpixel((x - 1, y - 1)) \
                    + imgbin.getpixel((x - 1, y)) \
                    + imgbin.getpixel((x - 1, y + 1)) \
                    + imgbin.getpixel((x, y - 1)) \
                    + cur_pixel \
                    + imgbin.getpixel((x, y + 1)) \
                    + imgbin.getpixel((x + 1, y - 1)) \
                    + imgbin.getpixel((x + 1, y)) \
                    + imgbin.getpixel((x + 1, y + 1))
                return 9 - sum

    def denoise(self):
        """
        image noise reduction
        """
        imgbin = self.grayscale()
        # 收集所有的噪点
        noise_point_list = []
        for x in range(imgbin.width):
            for y in range(imgbin.height):
                res_9 = self.__sum_9_region_new(imgbin, x, y)
                if (0 < res_9 < 3) and imgbin.getpixel((x, y)) == 0:  # 找到孤立点
                    pos = (x, y)
                    noise_point_list.append(pos)
        
        # 根据噪点的位置信息，消除二值图片的黑点噪声
        for item in noise_point_list:
            imgbin.putpixel((item[0], item[1]), 1)

        # save image
        out_buffer = BytesIO()
        imgbin.save(out_buffer, format='PNG')
        return base64.b64encode(out_buffer.getvalue())

