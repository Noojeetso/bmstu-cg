#include "wu_line.h"

inline int integer_part(double value)
{
    return floor(value);
}

inline double fract_part(double value)
{
    return value - floor(value);
}

inline double right_fract_part(double value)
{
    return 1 - fract_part(value);
}

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
            manager.add_point(integer_part(y), x, right_fract_part(y));
            manager.add_point(integer_part(y) + s, x, fract_part(y));
        }
        else {
            manager.add_point(x, integer_part(y), right_fract_part(y));
            manager.add_point(x, integer_part(y) + s, fract_part(y));
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
        _draw_line_wu(manager, a, b);
    }
    else
    {
        manager.add_point(a.x, a.y, MAX_INTENSITY);
    }

    return rc;
}
