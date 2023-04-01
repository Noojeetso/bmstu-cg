#ifndef BRESENHAM_LINE_FLOATING_POINT_H
#define BRESENHAM_LINE_FLOATING_POINT_H

#include "QPainter"
#include "QPen"
#include "errors.h"
#include "storage.h"
#include "math_impl.h"
#include "segment_check.h"

template<typename T>
ret_code_t add_line_bresenham_floating_point(T &manager, const Point &a, const Point &b);

extern template ret_code_t add_line_bresenham_floating_point<Canvas>(Canvas &canvas, const Point &a, const Point &b);

extern template ret_code_t add_line_bresenham_floating_point<Points>(Points &points, const Point &a, const Point &b);

#endif // BRESENHAM_LINE_FLOATING_POINT_H
