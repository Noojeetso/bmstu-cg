#include "graphicswidget.h"
#include "QDebug"
#include "segment_algorithms.h"
#include "QCoreApplication"

#include "QRect"

#define q_func() return static_cast<QWidget *>(q_ptr);

#define Q_Q(Class) Class * const q = q_func()


GraphicsWidget::GraphicsWidget(QWidget *parent):
    QWidget(parent)
{
//    this->points = new Points();
//    painter = new QPainter();
}

size_t step_counter = 0;

void GraphicsWidget::draw_rectangle(QPainter *painter, const QRect &rect)
{
    painter->drawRect(rect.x(), rect.y(), rect.width() - 1, rect.height() - 1);
}

void GraphicsWidget::do_update(void)
{
    QRect rect = this->rect();
    QCoreApplication::postEvent(this, new QEvent(QEvent::Paint));
//    QCoreApplication::postEvent(this, new QUpdateLaterEvent(rect));
}

void GraphicsWidget::paintEvent(QPaintEvent *event)
{
    ret_code_t rc;
    QWidget::paintEvent(event);
    size_t width, height;
    Point a;
    Point b;
//    QPainter *painter;
    QPainter painter(this);
    QPen pen;
//    Point current_point;

    width = event->rect().width();
    height = event->rect().height();

    a.x = 10;
    a.y = 10;
    b.x = width - 10;
    b.y = height - 10;

    qDebug() << event->rect() << width << height << "\n";

//    painter = new QPainter(this);
    painter.translate(0, height - 1);
    painter.scale(1, -1);
    pen = painter.pen();
    pen.setWidth(1);
    painter.setPen(pen);

    painter.save();

    draw_rectangle(&painter, event->rect());

    // draw_line_bresenham_floating_point(&painter, Line({this->a, this->b, MAX_INTENSITY}));

    // add_line_wu(&painter, this->a, this->b);
//    for (Points line: lines)
//    {
////        qDebug() << "liney\n";
//        for (Point point: line)
//        {
////            qDebug() << "pointy " << point.x << point.y << point.intensity << "\n";
//            pen.setColor(QColor(0, 0, 0, point.intensity));
//            painter->setPen(pen);
//            painter->drawPoint(point.x, point.y);
//        }
//    }
//    painter->drawLine(int(a.x), int(a.y),
//                      int(b.x), int(b.y));

    painter.restore();
    painter.end();
}
