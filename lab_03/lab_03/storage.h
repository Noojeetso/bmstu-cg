#ifndef STORAGE_H
#define STORAGE_H

#include <cstdlib>
#include <vector>
#include "QColor"
#include "errors.h"
#include <QString>
#include <QDebug>
#include <QGraphicsScene>

//#define DEFAULT_SIZE 128

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
//    Points(){}
//    ~Points(){}
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
//  Canvas(){}
public:
    QGraphicsScene scene;

    void add_point(int x, int y)
    {
        scene.addLine(x, y, x + 1, y);
    }
};

/*
class Points
{
public:
    Point *data;
    size_t length;
    size_t max_length;

    Points(void)
    {
//        ret_code_t rc;

        this->data = (Point*)malloc(sizeof(Point) * DEFAULT_SIZE);
        max_length = DEFAULT_SIZE;
        length = 0;

//        rc = points.data != NULL ? EXIT_OK : ERR_NULL_PTR;
//        return rc;
    }

    ret_code_t check_size(void)
    {
        return length < max_length ? EXIT_OK : ERR_OVERFLOW;
    }

    ret_code_t add_point(Point *point)
    {
        ret_code_t rc;

        rc = check_size();

        if (rc == ERR_OVERFLOW)
        {
            rc = expand();
        }

        if (rc == EXIT_OK)
        {
            data[length].x = point->x;
            data[length].y = point->y;
            data[length].intensity = 255;
            length++;
        }

        return rc;
    }

    ret_code_t add_point(int x, int y)
    {
        ret_code_t rc;

        rc = check_size();

        if (rc == ERR_OVERFLOW)
        {
            rc = expand();
        }

        if (rc == EXIT_OK)
        {
            data[length].x = x;
            data[length].y = y;
            data[length].intensity = 255;
            length++;
        }

        return rc;
    }

    ret_code_t add_point(int x, int y, int intensity)
    {
        ret_code_t rc;

        rc = check_size();

        if (rc == ERR_OVERFLOW)
        {
            rc = expand();
        }

        if (rc == EXIT_OK)
        {
            data[length].x = x;
            data[length].y = y;
            data[length].intensity = intensity;
            length++;
        }

        return rc;
    }

    ret_code_t expand(void)
    {
        ret_code_t rc;

        Point *new_data = (Point*)realloc(data, sizeof(Point) * max_length * 2);
        rc = new_data != NULL ? EXIT_OK : ERR_NO_MEMORY;

        if (rc == EXIT_OK)
        {
            data = new_data;
            max_length *= 2;
        }

        return EXIT_OK;
    }
};

class Lines
{
public:
    std::vector<Points*> lines;

    Lines(void){}
    ~Lines(void){}
};
*/


#endif // STORAGE_H
