QT       += core gui printsupport

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    analysis.cpp \
    bresenham_line_antialiased.cpp \
    bresenham_line_floating_point.cpp \
    bresenham_line_integer.cpp \
    digital_differential_analyzer.cpp \
    errors.cpp \
    graph.cpp \
    graphicswidget.cpp \
    library_line.cpp \
    main.cpp \
    mainwindow.cpp \
    math_impl.cpp \
    segment_algorithms.cpp \
    segment_check.cpp \
    storage.cpp \
    wu_line.cpp \
    qcustomplot.cpp

HEADERS += \
    analysis.h \
    bresenham_line_antialiased.h \
    bresenham_line_floating_point.h \
    bresenham_line_integer.h \
    digital_differential_analyzer.h \
    errors.h \
    graph.h \
    graphicswidget.h \
    library_line.h \
    mainwindow.h \
    math_impl.h \
    segment_algorithms.h \
    segment_check.h \
    storage.h \
    wu_line.h \
    qcustomplot.h

FORMS += \
    graph.ui \
    mainwindow.ui

CONFIG += lrelease
CONFIG += embed_translations

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target
