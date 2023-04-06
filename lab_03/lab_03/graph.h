#ifndef GRAPH_H
#define GRAPH_H

#include <QWidget>
#include "qcustomplot.h"

QT_BEGIN_NAMESPACE
namespace Ui { class Graph; }
QT_END_NAMESPACE

class Graph : public QWidget
{
    Q_OBJECT

public:
    Graph(void (*analyze)(QCustomPlot *plot, size_t iterations_amount, size_t segment_length), size_t iterations_amount, size_t segment_length, QWidget *parent = nullptr);
    ~Graph();

private:
    Ui::Graph *ui;
};

#endif // GRAPH_H
