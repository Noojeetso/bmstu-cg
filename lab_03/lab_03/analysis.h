#ifndef ANALYSIS_H
#define ANALYSIS_H

#include <QWidget>
#include "qcustomplot.h"

void analyze_speed(QCustomPlot *plot, size_t iterations_amount, size_t segment_length);

void analyze_stepping(QCustomPlot *plot, [[maybe_unused]] size_t iterations_amount, size_t segment_length);

#endif // ANALYSIS_H
