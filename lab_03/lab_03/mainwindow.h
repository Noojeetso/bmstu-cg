#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "storage.h"
#include "math_impl.h"
#include "segment_algorithms.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

    Canvas canvas;

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    template<typename T>
    ret_code_t add_line(T &manager, const Point &a, const Point &b);

//    ret_code_t add_line(Canvas &canvas, int idx, const Point &a, const Point &b);

private slots:
    void on_change_seg_color_clicked(void);

    void on_draw_seg_clicked(void);

    void on_draw_spectre_clicked();

private:
    Ui::MainWindow *ui;

//    ret_code_t add_line(Canvas &canvas, int idx, const Point &a, const Point &b);
//    template <> ret_code_t add_line(Canvas &canvas, const Point &a, const Point &b);

};
#endif // MAINWINDOW_H
