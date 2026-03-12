TEMPLATE = app
TARGET = myapp

QT += core gui widgets

CONFIG += c++17

SOURCES += \
    main.cpp \
    mainwindow.cpp \
    calculator.cpp

HEADERS += \
    mainwindow.h \
    calculator.h

FORMS += \
    mainwindow.ui

RESOURCES += \
    resources.qrc

# Include paths
INCLUDEPATH += include/

# Compiler flags
QMAKE_CXXFLAGS += -Wall -Wextra

# Platform-specific settings
win32 {
    RC_ICONS = myapp.ico
    QMAKE_TARGET_DESCRIPTION = "My Application"
}

macx {
    ICON = myapp.icns
    QMAKE_INFO_PLIST = Info.plist
}

unix:!macx {
    target.path = /usr/local/bin
    INSTALLS += target
}
