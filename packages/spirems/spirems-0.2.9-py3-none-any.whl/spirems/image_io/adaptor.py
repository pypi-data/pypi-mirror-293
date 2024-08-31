#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# @Author: renjin@bit.edu.cn
# @Date  : 2024-07-08

import time

try:
    import cv2
except Exception as e:
    print('Cannot import cv2 (pip install opencv-python)')

try:
    import av
except Exception as e:
    pass

import numpy as np
import base64
from spirems.msg_helper import get_all_msg_types, def_msg
from spirems.publisher import Publisher


def cvimg2sms(img: np.ndarray, format: str = 'jpeg', frame_id: str = 'camera') -> dict:
    assert len(img.shape) == 3 and img.shape[0] > 0 and img.shape[1] > 0 and img.shape[2] == 3 \
           and img.dtype == np.uint8, "CHECK img.ndim == 3 and img.dtype == np.uint8!"

    if format in ['jpeg', 'jpg', 'png', 'webp']:
        sms = def_msg('sensor_msgs::CompressedImage')
    elif format in ['h264']:
        sms = def_msg('sensor_msgs::CompressedImage')
    else:
        assert False, "Format ({}) is not supported".format(format)

    sms['timestamp'] = time.time()
    sms['frame_id'] = frame_id
    sms['format'] = format

    # t1 = time.time()
    if sms['format'] in ['jpeg', 'jpg']:
        success, img_encoded = cv2.imencode('.jpg', img)
    elif sms['format'] == 'png':
        success, img_encoded = cv2.imencode('.png', img)
    elif sms['format'] == 'webp':
        success, img_encoded = cv2.imencode('.webp', img, [cv2.IMWRITE_WEBP_QUALITY, 50])
    elif sms['format'] == 'h264':
        av_img = av.VideoFrame.from_ndarray(img, format="rgb24")
        codec = av.CodecContext.create('h264', 'w')
        codec.pix_fmt = "yuv420p"
        codec.width = img.shape[1]
        codec.height = img.shape[0]
        packet = codec.encode(av_img)
        while not len(packet):
            packet = codec.encode()
        img_encoded = bytes(packet[0])
    # print("-- imencode: {}".format(time.time() - t1))
    """
    elif sms['format'] == 'uint8':
        img_encoded = img.tobytes()
    """

    # t1 = time.time()
    img_base64 = base64.b64encode(img_encoded).decode('utf-8')
    # print("-- b64encode: {}".format(time.time() - t1))
    sms['data'] = img_base64

    return sms


def sms2cvimg(sms: dict) -> np.ndarray:
    assert sms['format'] in ['jpeg', 'jpg', 'png', 'webp', 'h264']
    assert sms['type'] == 'sensor_msgs::CompressedImage'
    img_base64 = base64.b64decode(sms['data'])
    if sms['format'] in ['jpeg', 'jpg', 'png', 'webp']:
        img_encoded = np.frombuffer(img_base64, dtype='uint8')
        img = cv2.imdecode(img_encoded, cv2.IMREAD_COLOR)
    elif sms['format'] in ['h264']:
        packet = av.packet.Packet(img_base64)
        codec = av.CodecContext.create(sms['format'], "r")
        imgs = codec.decode(packet)
        while not len(imgs):
            imgs = codec.decode()
        img = imgs[0].to_ndarray(format='rgb24')
        codec.close()
    else:
        assert False, "Format ({}) is not supported".format(sms['format'])
    """
    elif sms['format'] == 'uint8':
        img = np.frombuffer(img_base64, dtype='uint8')
        img = img.reshape(sms['height'], sms['width'], sms['channel'])
    """
    return img


if __name__ == '__main__':
    cap = cv2.VideoCapture(r'G:\Movie\001.mkv')
    # img1 = cv2.imread(r'C:\Users\jario\Pictures\2023-04-09-114628.png')
    pub = Publisher('/sensors/camera/image_raw', 'sensor_msgs::CompressedImage')
    while True:
        try:
            ret, img1 = cap.read()
            if not ret:
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue
            img1 = cv2.resize(img1, (1920, 800))
            sms = cvimg2sms(img1, format='h264')
            pub.publish(sms)
        except KeyboardInterrupt:
            print('stopped by keyboard')
            pub.kill()
            pub.join()
