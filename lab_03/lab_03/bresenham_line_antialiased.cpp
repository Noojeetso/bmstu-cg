#include "bresenham_line_antialiased.h"

template<typename T>
void _add_line_bresenham_antialiased(T &manager, const Point &a, const Point &b)
{
    int dx;
    int dy;
    double f_err;
    double W;
    const double intensity_levels = 1;

    dx = b.x - a.x;
    dy = b.y - a.y;

    const short sx = get_sign(dx);
    const short sy = get_sign(dy);

    dx = get_abs(dx);
    dy = get_abs(dy);

    const bool flipped = dx < dy;
    if (dy > dx)
    {
        std::swap(dx, dy);
    }

    const double tg = (double)dy / dx * intensity_levels;

    f_err = intensity_levels / 2;

    W = intensity_levels - tg;

    int x = a.x;
    int y = a.y;

    for (int i = 0; i < dx; i++)
    {
        manager.add_point(x, y, f_err);
        if (f_err <= W) {
            if (flipped)
                y += sy;
            else
                x += sx;
            f_err += tg;
        }
        else {
            x += sx;
            y += sy;
            f_err -= W;
        }

    }
}

template<typename T>
ret_code_t add_line_bresenham_antialiased(T &manager, const Point &a, const Point &b)
{
    ret_code_t rc;

    rc = check_segment(a, b);

    if (rc == EXIT_OK)
    {
        _add_line_bresenham_antialiased(manager, a, b);
    }
    else
    {
        manager.add_point(a.x, a.y, 1);
    }

    return rc;
}

template ret_code_t add_line_bresenham_antialiased<Canvas>(Canvas &canvas, const Point &a, const Point &b);

template ret_code_t add_line_bresenham_antialiased<Points>(Points &points, const Point &a, const Point &b);

template ret_code_t add_line_bresenham_antialiased<DummyManager>(DummyManager &manager, const Point &a, const Point &b);
