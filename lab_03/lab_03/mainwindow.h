#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "storage.h"
#include "math_impl.h"

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

private slots:
    void on_change_seg_color_clicked();

    void on_draw_seg_clicked();

    template<typename T>
    ret_code_t add_line(T &manager, const Point &a, const Point &b);

    void on_draw_spectre_clicked();

private:
    Ui::MainWindow *ui;
};
#endif // MAINWINDOW_H
