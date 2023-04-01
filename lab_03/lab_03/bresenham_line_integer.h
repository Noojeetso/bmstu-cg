#ifndef BRESENHAM_LINE_INTEGER_H
#define BRESENHAM_LINE_INTEGER_H

#include "QPainter"
#include "errors.h"
#include "storage.h"
#include "math_impl.h"
#include "segment_check.h"

template<typename T>
ret_code_t add_line_bresenham_integer(T &manager, const Point &a, const Point &b);

#endif // BRESENHAM_LINE_INTEGER_H
