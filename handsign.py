def judge_hand_sign(finger_num):
    if finger_num == 0:
        return "fist"
    elif finger_num == 1:
        return "one"
    elif finger_num == 2:
        return "two"
    elif finger_num == 3:
        return "palm"
    else:
        return "none"


def judge_hand_sign_from_color(color_list):
    if "green" in color_list and "yellow" in color_list:
        if color_list["green"] == 1 and color_list["yellow"] == 2:
            return "palm"
        elif color_list["yellow"] == 2:
            return "two"
        elif color_list["yellow"] == 1:
            return "one"
        else:
            return "fist"
    else:
        return "none"
