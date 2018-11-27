# coding: utf-8
# TODO: 用于去标签
# Author: chenhao
# data: 2018.11.26

# coding:utf-8

import numpy as np
import time
import numpngw
import cv2
# 去标签中的image painting问题
def regin_repair(img, pos):
    '''
    TODO:将标签位置补上
    :param img: 原图
    :param pos: 位置
    :return:
    '''
    mask = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)

    for i, j in zip(pos[0], pos[1]):
        mask[i, j] = 1
    img = img.astype(np.uint16)
    img_new = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

    return img_new






# 去标签
def removal_tag(ds):

    # 如果存在线形转换标签，则进行线形转换
    img = ds.pixel_array
    if hasattr(ds, "RescaleIntercept") and hasattr(ds, "RescaleSlope"):
        img = ds.RescaleSlope * img + ds.RescaleIntercept

    img = np.asarray(img, np.float)


    # 根据PresentationLUTShape 判断是否需要取反
    if hasattr(ds, "PresentationLUTShape") and hasattr(ds, "PhotometricInterpretation"):
        if ds[0x2050, 0x0020].value == "INVERSE" and ds[0x0028, 0x0004].value == "MONOCHROME1":

            vmin = img[img > 0].min()
            vmax = img.max()

            # 白色标签阈值
            whitetag = 0
            pos = np.where(img == whitetag)
            img = regin_repair(img, pos)
        else:
            # 白色标签阈值
            whitetag = pow(2, ds[0x0028, 0x0101].value) - 1
            whitetagwide = 5

            pos = np.where(img > (whitetag - whitetagwide))
            img = regin_repair(img, pos)


    else:
        # 白色标签阈值
        whitetag = pow(2, ds[0x0028, 0x0101].value) - 1
        whitetagwide = 5

        pos = np.where(img > (whitetag - whitetagwide))
        img = regin_repair(img, pos)

    return img



