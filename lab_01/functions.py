from math import sqrt, ceil, floor
from storage import Circle, Point


def define_circle(a, b, c, epsilon) -> Circle:
    b_radius_squared = b.x * b.x + b.y * b.y
    a_radius_squared = a.x * a.x + a.y * a.y
    c_radius_squared = c.x * c.x + c.y * c.y
    ab = (a_radius_squared - b_radius_squared) / 2
    bc = (b_radius_squared - c_radius_squared) / 2

    ba_x = a.x - b.x
    ba_y = a.y - b.y
    cb_x = b.x - c.x
    cb_y = b.y - c.y
    skew_product = ba_x * cb_y - cb_x * ba_y

    if abs(skew_product) < epsilon:
        raise ValueError

    cb_y = b.y - c.y
    ba_y = a.y - b.y
    center_x = (ab * cb_y - bc * ba_y) / skew_product
    ba_x = a.x - b.x
    cb_x = b.x - c.x
    center_y = (ba_x * bc - cb_x * ab) / skew_product

    radius = sqrt((center_x - a.x) ** 2 + (center_y - a.y) ** 2)

    return Circle(center_x, center_y, radius)


def min_round(num: float) -> float:
    if num > 0:
        return ceil(num)
    return floor(num)


def circle_in_ans(circles: list[Circle], new_circle: Circle, epsilon: float):
    return any(circle.is_equal(new_circle, epsilon) for circle in circles)


def get_circles(points: list[Point], epsilon: float) -> list[Circle]:
    circles: list[Circle] = list()
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            for k in range(j + 1, len(points)):
                p1 = points[i]
                p2 = points[j]
                p3 = points[k]

                try:
                    circle = define_circle(p1, p2, p3, epsilon)
                except ValueError:
                    continue
                if circle_in_ans(circles, circle, epsilon):
                    continue

                circles.append(circle)
    return circles


def filter_circles(circles: list[Circle], epsilon: float) -> tuple[list[Circle], list[float]]:
    used_circles = []
    line_heights = []
    for i in range(len(circles)):
        for j in range(i + 1, len(circles)):
            circle_a = circles[i]
            circle_b = circles[j]
            circle_added = False
            if abs(circle_a.y + circle_a.radius - (circle_b.y + circle_b.radius)) < epsilon:
                if not circle_in_ans(used_circles, circle_a, epsilon):
                    used_circles.append(circle_a)
                    circle_added = True
                if not circle_in_ans(used_circles, circle_b, epsilon):
                    used_circles.append(circle_b)
                    circle_added = True
                if circle_added:
                    line_heights.append(circle_a.y + circle_a.radius)

            if abs(circle_a.y - circle_a.radius - (circle_b.y - circle_b.radius)) < epsilon:
                if not circle_in_ans(used_circles, circle_a, epsilon):
                    used_circles.append(circle_a)
                    circle_added = True
                if not circle_in_ans(used_circles, circle_b, epsilon):
                    used_circles.append(circle_b)
                    circle_added = True
                if circle_added:
                    line_heights.append(circle_a.y - circle_a.radius)

    return used_circles, line_heights


def solve(left_points: list[Point], right_points: list[Point], epsilon: float) -> tuple[list[Circle], list[Circle], list[float]]:
    circles: list[Circle]
    circles = get_circles(left_points, epsilon)
    circles.extend(get_circles(right_points, epsilon))
    used_circles, line_heights = filter_circles(circles, epsilon)
    return circles, used_circles, line_heights
