#include "bresenham_line_integer.h"

template<typename T>
void _add_line_bresenham_integer(T &manager, const Point &a, const Point &b)
{
    int x;
    int y;
    int f_err;

    int dx = b.x - a.x;
    int dy = b.y - a.y;

    const short sx = get_sign(dx);
    const short sy = get_sign(dy);

    dx = get_abs(dx);
    dy = get_abs(dy);

    const bool flipped = dx < dy;
    if (flipped)
    {
        std::swap(dx, dy);
    }

    const int two_dx = 2 * dx;
    const int two_dy = 2 * dy;

    f_err = two_dy - dx;

    x = a.x;
    y = a.y;

    for (int i = 0; i < dx; i++)
    {
        manager.add_point(x, y, 1);

        if (f_err >= 0)
        {
            if (flipped)
                x += sx;
            else
                y += sy;
            f_err -= two_dx;
        }
        if (flipped)
            y += sy;
        else
            x += sx;
        f_err += two_dy;
    }
}

template<typename T>
ret_code_t add_line_bresenham_integer(T &manager, const Point &a, const Point &b)
{
    ret_code_t rc;

    rc = check_segment(a, b);

    if (rc == EXIT_OK)
    {
        _add_line_bresenham_integer(manager, a, b);
    }
    else
    {
        manager.add_point(a.x, a.y, 1);
    }

    return rc;
}

template ret_code_t add_line_bresenham_integer<Canvas>(Canvas &canvas, const Point &a, const Point &b);

template ret_code_t add_line_bresenham_integer<Points>(Points &points, const Point &a, const Point &b);

template ret_code_t add_line_bresenham_integer<DummyManager>(DummyManager &manager, const Point &a, const Point &b);
