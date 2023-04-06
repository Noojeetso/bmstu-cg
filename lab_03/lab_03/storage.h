#ifndef STORAGE_H
#define STORAGE_H

#include <cstdlib>
#include <vector>
#include "QColor"
#include "errors.h"
#include <QString>
#include <QDebug>
#include <QGraphicsScene>
#include <QGraphicsView>

struct Point
{
    int x;
    int y;
    int intensity;
};

struct Line
{
    Point a;
    Point b;
    QColor color;
};

class Points
{
public:
    std::vector<Point> data;

    void add_point(int x, int y, int intensity)
    {
        data.push_back(Point{x, y, intensity});
    }

    void clear(void)
    {
        data.clear();
    }
};

class Lines
{
public:
    std::vector<std::vector<Points>> data;
};

class Canvas
{
public:
    QGraphicsScene scene;
    QPen pen;
    QColor segment_color;
    QColor bg_color;
    QImage image;

    Canvas()
    {
        segment_color = Qt::black;
        bg_color = Qt::white;
    }

    void set_size(QSize &size)
    {
        image = QImage(size, QImage::Format_ARGB32);
        qDebug() << "resized: " << size << "\n";
        image.fill(bg_color);
    }

    void set_size(int x, int y)
    {
        QImage image = QImage(x, y, QImage::Format_ARGB32);
        qDebug() << "resized: " << x << " " << y << "\n";
        image.fill(bg_color);
    }

    void clear_scene(void)
    {
        scene.clear();
    }

    void clear_image(void)
    {
        image.fill(bg_color);
        update_image();
    }

    void update_image(void)
    {
//        scene.clear();
        scene.addPixmap(QPixmap::fromImage(image));
    }

    void set_segment_color(QColor &new_color)
    {
        segment_color = new_color;
        pen.setColor(segment_color);
    }

    void add_point(int x, int y, float intensity)
    {
        segment_color.setAlphaF(intensity);
        image.setPixel(x, y, segment_color.rgba());
    }
};

class DummyManager
{
public:
    void add_point([[maybe_unused]] int x, [[maybe_unused]] int y, [[maybe_unused]] float intensity){}
};

#endif // STORAGE_H
