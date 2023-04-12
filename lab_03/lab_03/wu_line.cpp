#include "wu_line.h"

template<typename T>
void _add_line_wu(T &manager, const Point &a, const Point &b) {
    int x1 = a.x;
    int y1 = a.y;
    int x2 = b.x;
    int y2 = b.y;

    const bool steep = abs(y2 - y1) > abs(x2 - x1);
    if (steep) {
        std::swap(x1,y1);
        std::swap(x2,y2);
    }
    if (x1 > x2) {
        std::swap(x1,x2);
        std::swap(y1,y2);
    }

    const double dx = x2 - x1;
    const double dy = y2 - y1;
    const double gradient = (dx == 0) ? 1 : dy / dx;

    // handle first endpoint
//    double x_end = round(x1);
//    double y_end = y1 + gradient * (x_end - x1);
//    double x_gap = get_right_fract_part(x1 + 0.5);
//    double x_px_loop1 = x_end;
//    double y_px_loop1 = get_integer_part(y_end);

//    if (steep) {
//        manager.add_point(y_px_loop1,     x_px_loop1,  get_right_fract_part(y_end) * x_gap);
//        manager.add_point(y_px_loop1 + 1, x_px_loop1,  get_fract_part(y_end) * x_gap);
//    } else {
//        manager.add_point(x_px_loop1, y_px_loop1,     get_right_fract_part(y_end) * x_gap);
//        manager.add_point(x_px_loop1, y_px_loop1 + 1, get_fract_part(y_end) * x_gap);
//    }

    // first y-intersection for the main loop
//    double y_intersection = y_end + gradient;

    // handle second endpoint
//    x_end = round(x2);
//    y_end = y2 + gradient * (x_end - x2);
//    x_gap = get_fract_part(x2 + 0.5);
//    double x_px_loop2 = x_end;
//    double y_px_loop2 = get_integer_part(y_end);

//    if (steep) {
//        manager.add_point(y_px_loop2,     x_px_loop2,  get_right_fract_part(y_end) * x_gap);
//        manager.add_point(y_px_loop2 + 1, x_px_loop2,  get_fract_part(y_end) * x_gap);
//    } else {
//        manager.add_point(x_px_loop2, y_px_loop2,     get_right_fract_part(y_end) * x_gap);
//        manager.add_point(x_px_loop2, y_px_loop2 + 1, get_fract_part(y_end) * x_gap);
//    }

    // main loop
    if (steep)
    {
        for (int x = x_px_loop1 + 1; x < x_px_loop2; x++)
        {
            manager.add_point(get_integer_part(y_intersection), x, get_right_fract_part(y_intersection));
            manager.add_point(get_integer_part(y_intersection) + 1, x, get_fract_part(y_intersection));
            y_intersection = y_intersection + gradient;
        }
    }
    else {
        for (int x = x_px_loop1 + 1; x < x_px_loop2; x++)
        {
            manager.add_point(x, get_integer_part(y_intersection), get_right_fract_part(y_intersection));
            manager.add_point(x, get_integer_part(y_intersection) + 1, get_fract_part(y_intersection));
            y_intersection = y_intersection + gradient;
        }
    }
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

template ret_code_t add_line_wu<DummyManager>(DummyManager &manager, const Point &a, const Point &b);
