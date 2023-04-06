#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include "storage.h"
#include "math_impl.h"
#include "segment_algorithms.h"
#include "analysis.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

    template<typename T>
    ret_code_t add_line(T &manager, const Point &a, const Point &b);

    void resizeEvent(QResizeEvent* event);

    void about(void);

//    ret_code_t add_line(Canvas &canvas, int idx, const Point &a, const Point &b);

private slots:
    void on_change_seg_color_clicked(void);

    void on_draw_seg_clicked(void);

    void on_draw_spectre_clicked();

    void on_analyze_speed_clicked();

    void on_analyze_steps_clicked();

    void on_clear_screen_clicked();

private:
    Ui::MainWindow *ui;
    Canvas canvas;
};
#endif // MAINWINDOW_H
