# -*- coding: utf-8 -*-
import cv2
import numpy as np
import color_detect as cd




# ブロブ解析
def analysis_blob(binary_img):
    # 2値画像のラベリング処理
    label = cv2.connectedComponentsWithStats(binary_img)

    # ブロブ情報を項目別に抽出
    n = label[0] - 1
    data = np.delete(label[2], 0, 0)
    center = np.delete(label[3], 0, 0)

    # ブロブ面積最大のインデックス
    max_index = np.argmax(data[:, 4])

    # 面積最大ブロブの情報格納用
    maxblob = {}

    # 面積最大ブロブの各種情報を取得
    maxblob["upper_left"] = (data[:, 0][max_index], data[:, 1][max_index])  # 左上座標
    maxblob["width"] = data[:, 2][max_index]  # 幅
    maxblob["height"] = data[:, 3][max_index]  # 高さ
    maxblob["area"] = data[:, 4][max_index]  # 面積
    maxblob["center"] = center[max_index]  # 中心座標

    return maxblob


def region_of_interest(mask):
    image, contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    rects = []
    for contour in contours:
        approx = cv2.convexHull(contour)
        rect = cv2.boundingRect(approx)
        rects.append(np.array(rect))

    return rects


def main():
    # カメラのキャプチャ
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        existing_color = []
        # フレームを取得
        ret, frame = cap.read()

        # 赤色検出
        red_mask = cd.detect_red(frame)
        cv2.imshow("Red Mask", red_mask)
        red_rects = region_of_interest(red_mask)
        if len(red_rects) > 0:
            rect = max(red_rects, key=(lambda x: x[2] * x[3]))
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 0, 255), thickness=2)
            print("red detected.")

        # 緑色検出
        green_mask = cd.detect_green(frame)
        cv2.imshow("Green Mask", green_mask)
        green_rects = region_of_interest(green_mask)
        if len(green_rects) > 0:
            rect = max(green_rects, key=(lambda x: x[2] * x[3]))
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (0, 255, 0), thickness=2)
            print("green detected.")

        # 青色検出
        blue_mask = cd.detect_blue(frame)
        cv2.imshow("Blue Mask", blue_mask)
        blue_rects = region_of_interest(blue_mask)
        if len(blue_rects) > 0:
            rect = max(blue_rects, key=(lambda x: x[2] * x[3]))
            cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 0, 0), thickness=2)
            print("blue detected.")

        # 白色検出
        # white_mask = cd.detect_white(frame)
        # cv2.imshow("White Mask", white_mask)
        # white_rects = region_of_interest(white_mask)
        # if len(white_rects) > 0:
        #     rect = max(white_rects, key=(lambda x: x[2] * x[3]))
        #     cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 0, 0), thickness=2)
        #     existing_color.append("white")
        # 結果表示
        cv2.imshow("Frame", frame)

        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
