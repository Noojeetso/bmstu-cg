#include "bresenham_line_floating_point.h"

template<typename T>
void _add_line_bresenham_floating_point(T &manager, const Point &a, const Point &b)
{
//    QColor color = origin_color;
//    QPen pen = painter.pen();
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
//        color.setAlpha(MAX_INTENSITY);
//        pen.setColor(color);
//        points->push_back({x, y, MAX_INTENSITY});
        manager.add_point(x, y, MAX_INTENSITY);

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
//    QPen pen = painter->pen();

    rc = check_segment(a, b);

    if (rc == EXIT_OK)
    {
        _draw_line_bresenham_floating_point(manager, a, b);
    }
    else
    {
//        pen.setColor(line.color);
//        painter->setPen(pen);
//        painter->drawPoint(line.a.x, line.a.y);
        manager.add_point(a.x, a.y, MAX_INTENSITY);
    }

    return rc;
}