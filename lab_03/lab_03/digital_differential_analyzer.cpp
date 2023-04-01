#include "digital_differential_analyzer.h"

template<typename T>
void _add_line_dda(T &manager, const Point &a, const Point &b)
{
    unsigned abs_x;
    unsigned abs_y;
    double length;
    double dx;
    double dy;
    double x;
    double y;

    abs_x = get_abs(b.x - a.x);
    abs_y = get_abs(b.y - a.y);

    length = abs_x;

    if (abs_y > abs_x)
    {
        length = abs_y;
    }

    dx = (b.x - a.x) / length;
    dy = (b.y - a.y) / length;

    x = a.x;
    y = a.y;

    for (size_t i = 1; i < length + 1; i++)
    {
        manager.add_point(int(x), int(y), 1);

        x += dx;
        y += dy;

        #ifdef STEP_COUNT
        step_counter++;
        #endif
    }
}

template<typename T>
ret_code_t add_line_dda(T &manager, const Point &a, const Point &b)
{
    ret_code_t rc;

    rc = check_segment(a, b);

    if (rc == EXIT_OK)
    {
        _add_line_dda(manager, a, b);
    }
    else
    {
        manager.add_point(a.x, a.y, 1);
    }

    return rc;
}

template ret_code_t add_line_dda<Canvas>(Canvas &canvas, const Point &a, const Point &b);

template ret_code_t add_line_dda<Points>(Points &points, const Point &a, const Point &b);
