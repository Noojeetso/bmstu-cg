#ifndef GRAPHICSWIDGET_H
#define GRAPHICSWIDGET_H

#include <QWidget>
#include <QPainter>
#include <QPaintEvent>

#include "math_impl.h"
#include "errors.h"
#include "storage.h"

class GraphicsWidget: public QWidget
{
    Q_OBJECT

public:
    GraphicsWidget(QWidget *parent);

    ~GraphicsWidget(){};

    Points points;
    Lines lines;
    Point a;
    Point b;

protected:
    virtual void paintEvent(QPaintEvent *);

private:
    void draw_rectangle(QPainter *painter, const QRect &rect);
};

#endif // GRAPHICSWIDGET_H
