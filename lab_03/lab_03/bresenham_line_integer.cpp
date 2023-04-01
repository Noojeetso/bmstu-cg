#include "bresenham_line_integer.h"

template<typename T>
void _add_line_bresenham_integer(T &manager, const Point &a, const Point &b)
{
    int tmp;
    int dx;
    int dy;
    int two_dx;
    int two_dy;
    int x;
    int y;
    short sx;
    short sy;
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

    two_dx = 2 * dx;
    two_dy = 2 * dy;

    f_err = two_dy - dx;

    x = a.x;
    y = a.y;

    for (int i = 1; i < dx + 1; i++)
    {
        manager.add_point(a.x, a.y, MAX_INTENSITY);

        if (f_err >= 0)
        {
            if (flipped)
                x += sx;
            else
                y += sy;
            f_err -= two_dx;
        }
        if (f_err <= 0)
        {
            if (flipped)
                y += sy;
            else
                x += sx;
            f_err += two_dy;
        }

        #ifdef STEP_COUNT
        step_counter++;
        #endif
    }
}

template<typename T>
ret_code_t add_line_bresenham_integer(T &manager, const Point &a, const Point &b)
{
    ret_code_t rc;

    rc = check_segment(a, b);

    if (rc == EXIT_OK)
    {
        _draw_line_bresenham_integer(manager, a, b);
    }
    else
    {
        manager.add_point(a.x, a.y, MAX_INTENSITY);
    }

    return rc;
}
