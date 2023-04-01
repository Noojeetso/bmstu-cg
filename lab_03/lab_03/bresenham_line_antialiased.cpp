#include "bresenham_line_antialiased.h"

template<typename T>
void _add_line_bresenham_smooth(T &manager, const Point &a, const Point &b)
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
    double W;
    bool flipped = false;
    int intensity_levels = MAX_INTENSITY;

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

    tg = (double)dy / dx * intensity_levels;

    f_err = intensity_levels / 2;

    W = intensity_levels - tg;

    x = a.x;
    y = a.y;

    for (int i = 0; i < dx; i++)
    {
        manager.add_point(x, y, int(f_err));

        if (f_err <= W)
        {
            if (flipped)
                y += sy;
            else
                x += sx;
            f_err += tg;
        }
        else if (f_err >= W)
        {
            x += sx;
            y += sy;
            f_err -= W;
        }

        #ifdef STEP_COUNT
        step_counter++;
        #endif
    }
}

template<typename T>
ret_code_t add_line_bresenham_smooth(T &manager, const Point &a, const Point &b)
{
    ret_code_t rc;

    rc = check_segment(a, b);

    if (rc == EXIT_OK)
    {
        _draw_line_bresenham_smooth(manager, a, b);
    }
    else
    {
        manager.add_point(a.x, a.y, MAX_INTENSITY);
    }

    return rc;
}
