#include "bresenham_line_floating_point.h"

template<typename T>
void _add_line_bresenham_floating_point(T &manager, const Point &a, const Point &b)
{
    int tmp;
    int dx;
    int dy;
    int x;
    int y;
    short sx;
    short sy;
    double tg;
    double f_err;
    bool flipped = false;

    dx = b.x - a.x;
    dy = b.y - a.y;

    sx = get_sign(dx);
    sy = get_sign(dy);

    dx = get_abs(dx);
    dy = get_abs(dy);

    if (dy > dx)
    {
        tmp = dx;
        dx = dy;
        dy = tmp;
        flipped = true;
    }

    tg = (double)dy / dx;

    f_err = tg - 0.5;

    x = a.x;
    y = a.y;

    for (int i = 1; i < dx + 1; i++)
    {
        manager.add_point(x, y, 1);

        if (f_err >= 0)
        {
            if (flipped)
                x += sx;
            else
                y += sy;
            f_err -= 1;
        }
        if (f_err <= 0)
        {
            if (flipped)
                y += sy;
            else
                x += sx;
            f_err += tg;
        }

        #ifdef STEP_COUNT
        step_counter++;
        #endif
    }
}

template<typename T>
ret_code_t add_line_bresenham_floating_point(T &manager, const Point &a, const Point &b)
{
    ret_code_t rc;

    rc = check_segment(a, b);

    if (rc == EXIT_OK)
    {
        _add_line_bresenham_floating_point(manager, a, b);
    }
    else
    {
        manager.add_point(a.x, a.y, 1);
    }

    return rc;
}

template ret_code_t add_line_bresenham_floating_point<Canvas>(Canvas &canvas, const Point &a, const Point &b);

template ret_code_t add_line_bresenham_floating_point<Points>(Points &points, const Point &a, const Point &b);
