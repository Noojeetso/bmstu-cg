#ifndef DIGITAL_DIFFERENTIAL_ANALYZER_H
#define DIGITAL_DIFFERENTIAL_ANALYZER_H

#include "QPainter"
#include "errors.h"
#include "storage.h"
#include "math_impl.h"
#include "segment_check.h"

template<typename T>
ret_code_t add_line_dda(T &manager, const Point &a, const Point &b);

#endif // DIGITAL_DIFFERENTIAL_ANALYZER_H
