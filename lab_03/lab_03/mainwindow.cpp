#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QColorDialog>
#include <QDebug>
#include "segment_algorithms.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->ui->graphicsView->setScene(&this->canvas.scene);
}

MainWindow::~MainWindow()
{
    delete ui;
}


void MainWindow::on_change_seg_color_clicked()
{
    QColor color = QColorDialog::getColor();
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

template<typename T>
ret_code_t MainWindow::add_line(T &manager, const Point &a, const Point &b)
{
    QString str = this->ui->algo_combobox->currentText();
    int idx = this->ui->algo_combobox->currentIndex();

    switch (idx)
    {
        case 0:
            draw_line_dda(manager, a, b);
            break;
        case 1:
            draw_line_bresenham_floating_point(manager, a, b);
            break;
        case 2:
            draw_line_bresenham_integer(manager, a, b);
            break;
        case 3:
            draw_line_bresenham_smooth(manager, a, b);
            break;
        case 4:
            draw_line_bresenham_smooth(manager, a, b);
            break;
    }

    return EXIT_OK;
}

void MainWindow::on_draw_seg_clicked()
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
        add_line(this->canvas);
    }
}


void MainWindow::on_draw_spectre_clicked()
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

    for (double current_angle_degrees = 0; rc == EXIT_OK && current_angle_degrees < 360; current_angle_degrees += step_degrees)
    {
        cos_a = get_cos(current_angle_degrees);
        sin_a = get_sin(current_angle_degrees);

        a.x = center.x - cos_a * segment_length / 2;
        b.x = center.x + cos_a * segment_length / 2;
        a.y = center.y - sin_a * segment_length / 2;
        b.y = center.y + sin_a * segment_length / 2;

        if (rc == EXIT_OK)
        {
            rc = fill_points_array(line, a, b);
        }
    }

    delete line;
}

