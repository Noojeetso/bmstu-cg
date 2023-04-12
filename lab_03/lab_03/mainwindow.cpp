#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QColorDialog>
#include <QDebug>
#include "qcustomplot.h"
#include "graph.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->ui->graphicsView->setScene(&this->canvas.scene);

    QSize size;
    size = this->ui->graphicsView->size();
//    canvas.setViewport(this->ui->graphicsView);
    canvas.set_size(size);

    QPixmap pixmap(16, 16);
    QPainter painter(&pixmap);

    pixmap.fill(canvas.segment_color);
    this->ui->change_seg_color->setIcon(pixmap);
    painter.drawRect(0, 0, 15, 15);

    connect(this->ui->action, &QAction::triggered, [=]() {
        about();
    });

//    pixmap.fill(canvas.bg_color);
//    painter.drawRect(0, 0, 15, 15);
//    this->ui->change_bg_color->setIcon(pixmap);
}

MainWindow::~MainWindow()
{
    delete ui;
}

void MainWindow::resizeEvent(QResizeEvent* event)
{
    QMainWindow::resizeEvent(event);

    qDebug() << event << "\n";
    QSize size;
    size = this->ui->graphicsView->size();
    canvas.set_size(size);

//    QRectF rect;
//    rect = this->ui->graphicsView->sceneRect();
//    canvas.set_size(rect.height(), rect.width());
}

void MainWindow::on_change_seg_color_clicked()
{
    QColor color;
    color = QColorDialog::getColor(color, this, "Выберите цвет");

    QPixmap pixmap(16, 16);
    QPainter painter(&pixmap);
    pixmap.fill(color);
    painter.drawRect(0, 0, 15, 15);
    this->ui->change_seg_color->setIcon(pixmap);
    canvas.set_segment_color(color);
}

ret_code_t get_int_from_field(int &value, const QLineEdit *field)
{
    ret_code_t rc;
    QString str;
    bool ok;

    if (field == NULL)
    {
        return ERR_NULL_PTR;
    }

    str = field->text();
    value = str.toInt(&ok);
    rc = ok ? EXIT_OK : ERR_INCORRECT_DATA;

    return rc;
}

ret_code_t get_size_t_from_field(size_t &value, const QLineEdit *field)
{
    ret_code_t rc;
    QString str;
    bool ok;

    if (field == NULL)
    {
        return ERR_NULL_PTR;
    }

    str = field->text();
    value = str.toULongLong(&ok);
    rc = ok ? EXIT_OK : ERR_INCORRECT_DATA;

    return rc;
}

template<typename T>
ret_code_t MainWindow::add_line(T &manager, const Point &a, const Point &b)
{
//        QString str = this->ui->algo_combobox->currentText();
    int idx = this->ui->algo_combobox->currentIndex();

    switch (idx)
    {
        case 0:
            add_line_dda(manager, a, b);
            break;
        case 1:
            add_line_bresenham_floating_point(manager, a, b);
            break;
        case 2:
            add_line_bresenham_integer(manager, a, b);
            break;
        case 3:
            add_line_bresenham_antialiased(manager, a, b);
            break;
        case 4:
            add_line_wu(manager, a, b);
            break;
        case 5:
            add_line_dda(manager, a, b);
            break;
    }

    return EXIT_OK;
}

template ret_code_t MainWindow::add_line<Canvas>(Canvas &canvas, const Point &a, const Point &b);

void MainWindow::on_draw_seg_clicked(void)
{
    ret_code_t rc;
    Point a;
    Point b;

    rc = get_int_from_field(a.x, this->ui->seg_begin_x);

    if (rc == EXIT_OK)
    {
        rc = get_int_from_field(a.y, this->ui->seg_begin_y);
    }

    if (rc == EXIT_OK)
    {
        rc = get_int_from_field(b.x, this->ui->seg_end_x);
    }

    if (rc == EXIT_OK)
    {
        rc = get_int_from_field(b.y, this->ui->seg_end_y);
    }

    if (rc == EXIT_OK)
    {
        add_line(this->canvas, a, b);
        this->canvas.update_image();
    }
}

void MainWindow::on_draw_spectre_clicked(void)
{
    ret_code_t rc;
    int segment_length;
    int step_degrees;
    Point center;

    double sin_a;
    double cos_a;
    Point a;
    Point b;
    Points *line = new Points();

    rc = get_int_from_field(center.x, this->ui->center_x);

    if (rc == EXIT_OK)
    {
        rc = get_int_from_field(center.y, this->ui->center_y);
    }

    if (rc == EXIT_OK)
    {
        rc = get_int_from_field(segment_length, this->ui->seg_length);
    }

    if (rc == EXIT_OK)
    {
        rc = get_int_from_field(step_degrees, this->ui->step_degrees);
    }

    for (double current_angle_degrees = 0; rc == EXIT_OK && current_angle_degrees < 180; current_angle_degrees += step_degrees)
    {
        cos_a = get_cos(current_angle_degrees);
        sin_a = get_sin(current_angle_degrees);

        a.x = center.x - cos_a * segment_length / 2;
        b.x = center.x + cos_a * segment_length / 2;
        a.y = center.y - sin_a * segment_length / 2;
        b.y = center.y + sin_a * segment_length / 2;

        if (rc == EXIT_OK)
        {
            add_line(this->canvas, a, b);
            this->canvas.update_image();
        }
    }

    delete line;
}

void MainWindow::on_analyze_speed_clicked()
{
    ret_code_t rc;
    size_t segment_length;
    size_t iterations_amount;

    rc = get_size_t_from_field(iterations_amount, this->ui->iter_amount);

    if (rc == EXIT_OK)
    {
        rc = get_size_t_from_field(segment_length, this->ui->test_seg_length);
    }

    if (rc == EXIT_OK)
    {
        Graph *graph = new Graph(analyze_speed, iterations_amount, segment_length, NULL);
    //    graph.setModal(true);
        graph->setWindowModality(Qt::WindowModal);
        graph->show();
    }
}


void MainWindow::on_analyze_steps_clicked()
{
    ret_code_t rc;
    size_t segment_length;
    size_t iterations_amount;

    rc = get_size_t_from_field(iterations_amount, this->ui->iter_amount);

    if (rc == EXIT_OK)
    {
        rc = get_size_t_from_field(segment_length, this->ui->test_seg_length);
    }

    if (rc == EXIT_OK)
    {
        Graph *graph = new Graph(analyze_stepping, iterations_amount, segment_length, NULL);
    //    graph.setModal(true);
        graph->setWindowModality(Qt::WindowModal);
        graph->show();
    }
}


void MainWindow::about(void)
{
    QMessageBox::about(this, "О программе", "Программа использует различные методы для отрисовки отрезков:\n"
                                            "На выбор пользователя предлагается нарисовать отрезок, спектр отрезков или провести анализ алгоритмов отображения отрезков\n\n"
                                            "Система координат оконная (центр в левом верхнем углу)\n"
                                            "Ось абсцисс направлена слева направо\n"
                                            "Ось ординат направлена сверху вниз\n\n"
                                            "Анализ ступенчатости:\n"
                                            "Необходимо задать длину отрезка для анализа\n"
                                            "Проверка осуществляется для отрезков с углом наклона\n"
                                            "от 0 до 360 градусов с шагом 1 градус\n\n"
                                            "Анализ скорости работы:\n"
                                            "Необходимо задать длину отрезка для анализа и количество итераций для повышения точности\n"
                                            "Проверка осуществляется для отрезков с углом наклона\n"
                                            "от 0 до 360 градусов с шагом 36 градусов");
}


void MainWindow::on_clear_screen_clicked()
{
    this->canvas.clear_image();
}

