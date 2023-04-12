#include "analysis.h"
#include <QDebug>
#include "storage.h"
#include "segment_algorithms.h"
#include <QElapsedTimer>
#include <algorithm>
#include<functional>
#include <map>

using namespace std;

typedef ret_code_t (*line_function_dummy_t)(DummyManager &manager, const Point &a, const Point &b);

typedef ret_code_t (*line_function_store_t)(Points &points, const Point &a, const Point &b);

//#define ITERATIONS_AMOUNT 1000
//#define SEGMENT_LENGTH 1000
#define MAX_ANGLE 360
#define STEP 10

class AlgorithmInfo
{
public:
    QString name;
    double elapsed_time;
    int steps_amount;

    AlgorithmInfo(QString name)
    {
        this->name = name;
    }
};

class AlgorithmsInfo
{
public:
    QVector<AlgorithmInfo> data;

    QVector<QString> labels;
    QVector<double> elapsed_time;
    QVector<double> steps_amount;

    AlgorithmsInfo(QVector<QString> &names)
    {
        for (QString name: names)
        {
            data.push_back(AlgorithmInfo(name));
        }
    }

    AlgorithmInfo& operator[](int index)
    {
        return data[index];
    }

    void sort_by_time(void)
    {
        std::sort(begin(data), end(data),
                  [](AlgorithmInfo a, AlgorithmInfo b) { return a.elapsed_time < b.elapsed_time; });
    }

    void sort_by_steps(void)
    {
        std::sort(begin(data), end(data),
                  [](AlgorithmInfo a, AlgorithmInfo b) { return a.steps_amount > b.steps_amount; });
    }

    QVector<QString>& get_labels(void)
    {
        labels.clear();
        for (AlgorithmInfo info: data)
        {
            labels.push_back(info.name);
        }
        return labels;
    }

    QVector<double>& get_elapsed_time(void)
    {
        elapsed_time.clear();
        for (AlgorithmInfo info: data)
        {
            elapsed_time.push_back(info.elapsed_time);
        }
        return elapsed_time;
    }

    QVector<double>& get_steps_amount(void)
    {
        steps_amount.clear();
        for (AlgorithmInfo info: data)
        {
            steps_amount.push_back(info.steps_amount);
        }
        return steps_amount;
    }
};

void analyze_speed(QCustomPlot *plot, size_t iterations_amount, size_t segment_length)
{
    QElapsedTimer timer;
    DummyManager manager;
    QPixmap pixmap(segment_length, segment_length);
    QPainter painter(&pixmap);

    Point a;
    Point b;
    QPoint q_a;
    QPoint q_b;

    double cos_a;
    double sin_a;
    double current_angle_degrees;
    const size_t angles_amount = MAX_ANGLE / STEP;

    QVector<QString> labels = {"ЦДА", "Брезенхем\n(числа с плавающей точкой)", "Брезенхем\n(целые числа)", "Брезенхем\n(со сглаживанием)", "Ву", "Библиотечная"};
    line_function_dummy_t functions [] =
    {
        add_line_dda,
        add_line_bresenham_floating_point,
        add_line_bresenham_integer,
        add_line_bresenham_antialiased,
        add_line_wu
    };

    AlgorithmsInfo algorithms_info = AlgorithmsInfo(labels);

    for (size_t i = 0; i < sizeof(functions) / sizeof(functions[0]); i++)
    {
        current_angle_degrees = 0;
        for (size_t j = 0; j < angles_amount; j++)
        {
            cos_a = get_cos(current_angle_degrees);
            sin_a = get_sin(current_angle_degrees);

            a.x = segment_length - cos_a * segment_length / 2;
            b.x = segment_length + cos_a * segment_length / 2;
            a.y = segment_length - sin_a * segment_length / 2;
            b.y = segment_length + sin_a * segment_length / 2;

            timer.start();

            for (size_t k = 0; k < iterations_amount; k++)
            {
                functions[i](manager, a, b);
            }

            algorithms_info[i].elapsed_time += timer.nsecsElapsed() / iterations_amount;

            current_angle_degrees += STEP;
        }
        algorithms_info[i].elapsed_time /= angles_amount;
    }

    current_angle_degrees = 0;
    for (size_t j = 0; j < angles_amount; j++)
    {
        cos_a = get_cos(current_angle_degrees);
        sin_a = get_sin(current_angle_degrees);

        q_a.setX(segment_length - cos_a * segment_length / 2);
        q_b.setX(segment_length + cos_a * segment_length / 2);
        q_a.setY(segment_length - sin_a * segment_length / 2);
        q_b.setY(segment_length + sin_a * segment_length / 2);

        timer.start();

        for (size_t k = 0; k < iterations_amount; k++)
        {
            painter.drawLine(q_a, q_b);
        }

        algorithms_info[sizeof(functions) / sizeof(functions[0])].elapsed_time += timer.nsecsElapsed() / iterations_amount;

        current_angle_degrees += STEP;
    }
    algorithms_info[sizeof(functions) / sizeof(functions[0])].elapsed_time /= angles_amount;

    algorithms_info.sort_by_time();

    QVector<double> ticks;
    ticks << 1 << 2 << 3 << 4 << 5 << 6;

    QSharedPointer<QCPAxisTickerText> textTicker(new QCPAxisTickerText);
    textTicker->addTicks(ticks, algorithms_info.get_labels());
    plot->xAxis->setTicker(textTicker);

    plot->yAxis->setLabel("Время в наносекундах");

    QCPBars *time = new QCPBars(plot->xAxis, plot->yAxis);
    time->setData(ticks, algorithms_info.get_elapsed_time());

    plot->xAxis->setRange(0, ticks.length() + 1);
    plot->yAxis->setRange(0, *std::max_element(algorithms_info.get_elapsed_time().begin(), algorithms_info.get_elapsed_time().end()) * 1.1);

    plot->replot();
    plot->update();
}

size_t count_steps(Points &points)
{

    Point point;
    point = points.data[0];
    int x_prev = point.x;
    int y_prev = point.y;
    int x;
    int y;
    size_t cnt = 0;
    for (size_t i = 1; i < points.data.size(); i++)
    {
        point = points.data[i];

        x = point.x;
        y = point.y;

        if (x != x_prev && y != y_prev)
        {
            cnt++;
        }

        x_prev = x;
        y_prev = y;
    }
    return cnt;
}

void analyze_stepping(QCustomPlot *plot, [[maybe_unused]] size_t iterations_amount, size_t segment_length)
{
    Points points = Points();
    map<QString,int> step_map;

    Point a;
    Point b;

    double cos_a;
    double sin_a;
    double current_angle_degrees;
    const size_t angles_amount = MAX_ANGLE / 4;

    line_function_store_t functions [] =
    {
        add_line_dda,
        add_line_bresenham_floating_point,
        add_line_bresenham_integer
    };

    QVector<QVector<double>> steps_amounts(sizeof(functions) / sizeof(functions[0]));
    QVector<double> *current_amounts;

    size_t current_steps_amount;

    for (size_t i = 0; i < sizeof(functions) / sizeof(functions[0]); i++)
    {
        current_amounts = &steps_amounts[i];
        current_angle_degrees = 0;
        for (size_t j = 0; j <= angles_amount; j++)
        {
            cos_a = get_cos(current_angle_degrees);
            sin_a = get_sin(current_angle_degrees);

            a.x = segment_length - cos_a * segment_length / 2;
            b.x = segment_length + cos_a * segment_length / 2;
            a.y = segment_length - sin_a * segment_length / 2;
            b.y = segment_length + sin_a * segment_length / 2;

            points.clear();
            functions[i](points, a, b);
            current_steps_amount = count_steps(points);
            current_amounts->append(current_steps_amount);

            current_angle_degrees += 1;
        }
    }

    QVector<double> x_ticks;

    current_angle_degrees = 0;
    for (size_t j = 0; j <= angles_amount; j++)
    {
        x_ticks << j;
        current_angle_degrees += 1;
    }

    QPen pen;
    const int scale = 1;

    pen = QPen(QColor(0xff, 0, 0), 2);
    plot->addGraph();
    plot->graph(0)->setPen(pen);

    pen = QPen(QColor(0, 0xff, 0), 2);
    pen.setDashPattern({ 0.0, 4.0 * scale, 1.0 * scale, 4.0 * scale});
    plot->addGraph();
    plot->graph(1)->setPen(pen);

    pen = QPen(QColor(0, 0, 0xff), 2);
    plot->addGraph();
    pen.setDashPattern({ 0.0, 1.0 * scale, 1.0 * scale, 7.0 * scale });
    plot->graph(2)->setPen(pen);

    plot->graph(0)->setName("ЦДА");
    plot->graph(1)->setName("Брезенхем (числа с плавающей точкой)");
    plot->graph(2)->setName("Брезенхем (целые числа)");
    plot->xAxis->setLabel("Угол в градусах");
    plot->yAxis->setLabel("Количество ступенек");

    QVector<double> y_ticks;
    plot->graph(0)->setData(x_ticks, steps_amounts[0]);
    plot->graph(1)->setData(x_ticks, steps_amounts[1]);
    plot->graph(2)->setData(x_ticks, steps_amounts[2]);
    plot->graph(0)->rescaleAxes();

    plot->xAxis->setRange(0, 100);
    plot->yAxis->setRange(0, *std::max_element(steps_amounts[1].begin(), steps_amounts[1].end()) * 1.1);

    plot->legend->setVisible(true);
    plot->axisRect()->insetLayout()->setInsetAlignment(0, Qt::AlignTop|Qt::AlignHCenter|Qt::AlignLeft);
    plot->legend->setBrush(QColor(255, 255, 255, 100));
    plot->legend->setBorderPen(Qt::NoPen);

    plot->replot();
    plot->update();
}
