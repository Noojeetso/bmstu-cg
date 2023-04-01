#ifndef BRESENHAM_LINE_ANTIALIASED_H
#define BRESENHAM_LINE_ANTIALIASED_H

#include "QPainter"
#include "errors.h"
#include "storage.h"
#include "math_impl.h"
#include "segment_check.h"

template<typename T>
ret_code_t add_line_bresenham_smooth(T &manager, const Point &a, const Point &b);

#endif // BRESENHAM_LINE_ANTIALIASED_H
