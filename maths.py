import math as mt


def multiply(coef: int, vector: list) -> list:
    return [coef * vector[0], coef * vector[1]]


def add(vec1: list, vec2: list) -> list:
    return [vec1[0] + vec2[0], vec1[1] + vec2[1]]


def write(vec: list, row: int) -> None:
    print(vec[row])
    return


def copy(tuple: tuple) -> list:
    return [tuple[0], tuple[1]]


def isLarge(vec: list, limit: int) -> bool:
    if vec[0] > limit or vec[1] > limit:
        return True
    else:
        return False


def sort(list_: list) -> list:
    x_list = []
    y_list = []
    for i in range(len(list_)):
        for j in list_[i]:
            x_list.append(list_[i][0])
            y_list.append(list_[i][1])
    return [x_list, y_list]


def velocity(time_step: int, grav_parameter: int, point: list, vel_now: list) -> list:
    epsilon = 1 / mt.sqrt(pow(point[0], 2) + pow(point[1], 2))
    sn = multiply(epsilon, [-point[0], -point[1]])
    ac = grav_parameter * pow(epsilon, 2)
    ac_vec = multiply(ac, sn)
    if isLarge(vel_now, 10000000):
        return vel_now
    else:
        return add(multiply(time_step, ac_vec), vel_now)


def point_calc(time_step: int, point: list, vel_now: list) -> list:
    return add(multiply(time_step, vel_now), point)
