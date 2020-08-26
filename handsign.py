def judge_hand_sign(part_list):
    if "finger" in part_list and "palm" in part_list:
        if part_list["palm"] == 1 and part_list["finger"] == 4:
            return "open"
        elif part_list["finger"] == 4:
            return "four"
        elif part_list["finger"] == 3:
            return "three"
        elif part_list["finger"] == 2:
            return "two"
        elif part_list["finger"] == 1:
            return "one"
        else:
            return "close"
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
