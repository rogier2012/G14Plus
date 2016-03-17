import sys


def branchingrule0(alpha_list):
    color = None
    for color_list in alpha_list:
        if len(color_list) >= 4:
            color = color_list
            break

    return color


def branchingrule1(alpha_list):
    color = None
    length = 2
    for color_list in alpha_list:
        if len(color_list) > length:
            color = color_list
            length = len(color_list)
    return color


def branchingrule2(alpha_list):
    color = None
    length = sys.maxsize
    for color_list in alpha_list:
        if len(color_list) <= length and len(color_list) >= 4:
            color = color_list
            length = len(color_list)
    return color


def branchingrule3(alpha_list):
    color = None
    maxdegree = 0
    for color_list in alpha_list:
        if len(color_list) >= 4 and color_list[0].deg() > maxdegree:
            color = color_list
            maxdegree = color_list[0].deg()
    return color
