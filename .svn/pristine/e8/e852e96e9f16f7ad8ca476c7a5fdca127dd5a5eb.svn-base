# -*- coding:utf-8 -*-
 
#知识点：二维码生成，图片合成，图片处理，web前后端交互
 
import sys
import qrcode
import time
 
#生成二维码函数，传入信息参数
def qc(url):
    #创建qrcode对象
    qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=8,
        border=4,
        )
    #version为一个整数，范围1~40，作用表示二维码的大小
    #error_correction容错率，挡出部分二维码还能识别，越高可以挡住部分越多，但数据量增加
    #四个等级：H,L,M,Q  Q最高，可以挡住25%
    #box_size 每个格子里像素大小
    #border 表示二维码距离图像外边框的距离
    qr.add_data(url)
    qr.make(fit=True)
    img=qr.make_image() #创建二维码图片
    img=img.convert("RGBA") #图片转换为RGBA格式
    path = "/static/imgcard/%s.png" %time.time()
    img.save("./zs_backend%s" % path)#保存图片

    return path
    