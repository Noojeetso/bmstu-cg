#ifndef STORAGE_H
#define STORAGE_H

#include <cstdlib>
#include <vector>
#include "QColor"
#include "errors.h"
#include <QString>
#include <QDebug>
#include <QGraphicsScene>

#define MAX_INTENSITY 255

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

    void add_point(int x, int y)
    {
        scene.addLine(x, y, x + 1, y);
    }
};

#endif // STORAGE_H
