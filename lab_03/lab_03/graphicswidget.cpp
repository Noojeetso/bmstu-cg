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
}

size_t step_counter = 0;

void GraphicsWidget::draw_rectangle(QPainter *painter, const QRect &rect)
{
    painter->drawRect(rect.x(), rect.y(), rect.width() - 1, rect.height() - 1);
}

void GraphicsWidget::paintEvent(QPaintEvent *event)
{
    QWidget::paintEvent(event);
    size_t width, height;
    QPainter painter(this);
    QPen pen;

    width = event->rect().width();
    height = event->rect().height();

    a.x = 10;
    a.y = 10;
    b.x = width - 10;
    b.y = height - 10;

    qDebug() << event->rect() << width << height << "\n";

    painter.translate(0, height - 1);
    painter.scale(1, -1);
    pen = painter.pen();
    pen.setWidth(1);
    painter.setPen(pen);

    painter.save();

    draw_rectangle(&painter, event->rect());

    painter.restore();
    painter.end();
}
