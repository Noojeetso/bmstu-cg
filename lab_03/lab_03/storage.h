#ifndef STORAGE_H
#define STORAGE_H

#include <cstdlib>
#include <vector>
#include "QColor"
#include "errors.h"
#include <QString>
#include <QDebug>
#include <QGraphicsScene>

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
    QBrush brush;
    QColor color;
    QPen pen;

    Canvas()
    {
        brush = scene.foregroundBrush();
        color = brush.color();
    }

    void add_point(int x, int y, float intensity)
    {
        color.setAlphaF(intensity);
//        brush.setColor(color);
//        scene.setForegroundBrush(brush)
        pen.setColor(color);
        scene.addLine(x, y, x + 1, y, pen);
    }
};

#endif // STORAGE_H
