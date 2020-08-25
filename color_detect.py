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

