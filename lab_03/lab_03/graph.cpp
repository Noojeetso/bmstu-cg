#include "graph.h"
#include "ui_graph.h"
#include "analysis.h"
#include <QDebug>

Graph::Graph(void (*analyze)(QCustomPlot *plot, size_t iterations_amount, size_t segment_length), size_t iterations_amount, size_t segment_length, QWidget *parent)
    : QWidget(parent)
    , ui(new Ui::Graph)
{
    ui->setupUi(this);

    connect(ui->customPlot->xAxis, SIGNAL(rangeChanged(QCPRange)), ui->customPlot->xAxis2, SLOT(setRange(QCPRange)));
    connect(ui->customPlot->yAxis, SIGNAL(rangeChanged(QCPRange)), ui->customPlot->yAxis2, SLOT(setRange(QCPRange)));

    ui->customPlot->setInteractions(QCP::iRangeDrag | QCP::iRangeZoom | QCP::iSelectPlottables);

    analyze(this->ui->customPlot, iterations_amount, segment_length);
}

Graph::~Graph()
{
    delete ui;
}
