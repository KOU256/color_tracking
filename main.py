# -*- coding: utf-8 -*-
import cv2
import numpy as np
import color_detect as cd
import mouse
import handsign as hs


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
    cv2.namedWindow("Frame", cv2.WINDOW_AUTOSIZE)
    fgbg = cv2.createBackgroundSubtractorMOG2()
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
    mouse_data = mouse.Mouse("Frame")
    targets =[]

    while cap.isOpened():
        ret, frame = cap.read()

        if mouse_data.getEvent() == cv2.EVENT_LBUTTONUP:
            h, s, v = cd.get_cursor_position_color(frame, mouse_data.getX(), mouse_data.getY())
            if len(targets) == 0:
                target = {"part": "finger", "h": h, "s": s, "v": v}
            else:
                target = {"part": "palm", "h": h, "s": s, "v": v}
            targets.append(target)
        elif mouse_data.getEvent() == cv2.EVENT_RBUTTONUP:
            targets.clear()

        fgmask = fgbg.apply(frame)
        _, fgmask = cv2.threshold(fgmask, 127, 1, cv2.THRESH_BINARY)
        fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
        bgr = cv2.split(frame)
        new_bgr = list(map(lambda x:x * fgmask, bgr))
        result = cv2.merge(new_bgr)

        part_list = {}
        for target in targets:
            mask = cd.detect_color(result, target["h"], target["s"], target["v"])
            rects = region_of_interest(mask)
            part = target["part"]
            part_list[part] = 0

            if len(rects) > 0:
                if part == "finger":
                    for rect in rects:
                        if rect[2] * rect[3] >= 150:
                            cv2.rectangle(result, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 255, 255), thickness=2)
                            part_list[part] += 1
                elif part == "palm":
                    rect = max(rects, key=(lambda x: x[2] * x[3]))
                    if rect[2] * rect[3] >= 150:
                        cv2.rectangle(result, tuple(rect[0:2]), tuple(rect[0:2] + rect[2:4]), (255, 255, 255), thickness=2)
                        part_list[part] += 1

        cv2.putText(result, "HandSign:" + hs.judge_hand_sign(part_list), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), thickness=1)

        # 結果表示
        cv2.imshow("Frame", result)

        # qキーが押されたら途中終了
        if cv2.waitKey(25) & 0xFF == ord('q') or not ret:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
