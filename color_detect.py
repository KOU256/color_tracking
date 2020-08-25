# -*- coding: utf-8 -*-
import cv2
import numpy as np


def detect_red(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 赤色のHSVの値域1
    hsv_min = np.array([0, 64, 127])
    hsv_max = np.array([30, 255, 255])
    mask1 = cv2.inRange(hsv, hsv_min, hsv_max)

    # 赤色のHSVの値域2
    hsv_min = np.array([150, 64, 127])
    hsv_max = np.array([179, 255, 255])
    mask2 = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask1 + mask2


def detect_green(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 緑色のHSVの値域
    hsv_min = np.array([30, 127, 127])
    hsv_max = np.array([90, 255, 255])
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask


def detect_blue(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 青色のHSVの値域
    hsv_min = np.array([90, 64, 127])
    hsv_max = np.array([150, 255, 255])
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask


def detect_white(img):
    # HSV色空間に変換
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 白色のHSVの値域
    hsv_min = np.array([0, 0, 127])
    hsv_max = np.array([32, 32, 255])
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask


def detect_color(img, h, s, v):
    h_border = 15
    s_border = 50
    v_border = 50
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    hsv_min = np.array([h - h_border, max(127, s - s_border), max(127, v - v_border)])
    hsv_max = np.array([h + h_border, min(255, s + s_border), max(255, v + v_border)])
    mask = cv2.inRange(hsv, hsv_min, hsv_max)

    return mask


def get_color_from_hsv(h, s, v):
    if 80 < h < 110 and 127 < s <= 255 and 127 < v <= 255:
        return "yellow"
    elif 30 < h < 50 and 127 < s <= 255 and 127 < v <= 255:
        return "green"
    else:
        return "other"


def get_cursor_position_color(img, x, y):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    h = int(hsv.item(y, x, 0))
    s = int(hsv.item(y, x, 1))
    v = int(hsv.item(y, x, 2))

    print("HSV: %d %d %d" % (h, s, v))

    return get_color_from_hsv(h, s, v), h, s, v
