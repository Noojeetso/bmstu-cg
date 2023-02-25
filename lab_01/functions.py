import math
from math import sqrt, ceil, floor


def define_circle(p1, p2, p3, epsilon) -> tuple[tuple[float, float], float]:
    temp = p2[0] * p2[0] + p2[1] * p2[1]
    bc = (p1[0] * p1[0] + p1[1] * p1[1] - temp) / 2
    cd = (temp - p3[0] * p3[0] - p3[1] * p3[1]) / 2
    det = (p1[0] - p2[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p2[1])

    if abs(det) < epsilon:
        return (float("nan"), float("nan"), ), float("nan")

    cx = (bc * (p2[1] - p3[1]) - cd * (p1[1] - p2[1])) / det
    cy = ((p1[0] - p2[0]) * cd - (p2[0] - p3[0]) * bc) / det

    radius = sqrt((cx - p1[0]) ** 2 + (cy - p1[1]) ** 2)
    return (cx, cy), radius


def min_round(num: float) -> float:
    if num > 0:
        return ceil(num)
    return floor(num)


def circle_in_ans(ans, src_circle, epsilon: float):
    for circle in ans:
        if abs(circle[0][0] - src_circle[0][0]) >= epsilon or \
           abs(circle[0][1] - src_circle[0][1]) >= epsilon or \
           abs(circle[1] - src_circle[1]) >= epsilon:
            continue
        return True
    return False


def solve(left_points, right_points, epsilon: float):
    circles: list[tuple[tuple[float, float], float]] = list()
    for p1 in left_points:
        for p2 in left_points:
            for p3 in left_points:
                circle_left = define_circle([p1.x, p1.y], [p2.x, p2.y], [p3.x, p3.y], epsilon)
                if math.isnan(circle_left[1]):
                    continue
                if circle_in_ans(circles, circle_left, epsilon):
                    continue
                # print("circle left", circle_left)
                circles.append(circle_left)
    for p1 in right_points:
        for p2 in right_points:
            for p3 in right_points:
                circle_right = define_circle([p1.x, p1.y], [p2.x, p2.y], [p3.x, p3.y], epsilon)
                if math.isnan(circle_right[1]):
                    continue
                if circle_in_ans(circles, circle_right, epsilon):
                    continue
                # print("circle right", circle_right)
                circles.append(circle_right)

    used_circles = []
    line_heights = []
    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            circle_a = circles[i]
            circle_b = circles[j]
            if abs(circle_a[0][1] + circle_a[1] - (circle_b[0][1] + circle_b[1])) < epsilon:
                line_heights.append(circle_a[0][1] + circle_a[1])
                used_circles.append(circle_a)
                used_circles.append(circle_b)
            if abs(circle_a[0][1] + circle_a[1] - (circle_b[0][1] - circle_b[1])) < epsilon:
                line_heights.append(circle_a[0][1] + circle_a[1])
                used_circles.append(circle_a)
                used_circles.append(circle_b)
            if abs(circle_a[0][1] - circle_a[1] - (circle_b[0][1] + circle_b[1])) < epsilon:
                line_heights.append(circle_a[0][1] - circle_a[1])
                used_circles.append(circle_a)
                used_circles.append(circle_b)
            if abs(circle_a[0][1] - circle_a[1] - (circle_b[0][1] - circle_b[1])) < epsilon:
                line_heights.append(circle_a[0][1] - circle_a[1])
                used_circles.append(circle_a)
                used_circles.append(circle_b)

    return circles, used_circles, line_heights
