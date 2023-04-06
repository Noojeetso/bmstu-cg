#ifndef WU_LINE_H
#define WU_LINE_H

#include "QPainter"
#include "errors.h"
#include "storage.h"
#include "math_impl.h"
#include "segment_check.h"

template<typename T>
ret_code_t add_line_wu(T &manager, const Point &a, const Point &b);

extern template ret_code_t add_line_wu<Canvas>(Canvas &canvas, const Point &a, const Point &b);

extern template ret_code_t add_line_wu<Points>(Points &points, const Point &a, const Point &b);

extern template ret_code_t add_line_wu<DummyManager>(DummyManager &manager, const Point &a, const Point &b);

#endif // WU_LINE_H
