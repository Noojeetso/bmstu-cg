#include "wu_line.h"

template<typename T>
bool _add_line_wu(T &manager, const Point &a, const Point &b)
{
    int x1 = a.x;
    int y1 = a.y;
    int x2 = b.x;
    int y2 = b.y;

    int dx = x2 - x1;
    int dy = y2 - y1;

    const bool swapped = qAbs(dx) < qAbs(dy);
    if (swapped) {
        qSwap(x1, y1);
        qSwap(x2, y2);
        qSwap(dx, dy);
    }
    if (x2 < x1) {
        qSwap(x1, x2);
        qSwap(y1, y2);
    }

    dx = x2 - x1;
    dy = y2 - y1;
    double grad = dx ? static_cast<double>(dy) / dx : 1;

    double y = y1;
    for (int x = x1; x <= x2; ++x)
    {
        const int s = get_sign(y);
        if (swapped)
        {
            manager.add_point(get_integer_part(y), x, get_right_fract_part(y));
            manager.add_point(get_integer_part(y) + s, x, get_fract_part(y));
        }
        else {
            manager.add_point(x, get_integer_part(y), get_right_fract_part(y));
            manager.add_point(x, get_integer_part(y) + s, get_fract_part(y));
        }
        y += grad;
    }

    return true;
}

template<typename T>
ret_code_t add_line_wu(T &manager, const Point &a, const Point &b)
{
    ret_code_t rc;

    rc = check_segment(a, b);

    if (rc == EXIT_OK)
    {
        _add_line_wu(manager, a, b);
    }
    else
    {
        manager.add_point(a.x, a.y, 1);
    }

    return rc;
}

template ret_code_t add_line_wu<Canvas>(Canvas &canvas, const Point &a, const Point &b);

template ret_code_t add_line_wu<Points>(Points &points, const Point &a, const Point &b);
