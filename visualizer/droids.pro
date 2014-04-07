INCLUDEPATH +=  ../interfaces                 ../common/                 ./parser/

DEPENDPATH += ../common/ 

TEMPLATE = lib
TARGET = droids
SOURCES = *.cpp           ./parser/*.cpp           ./parser/sexp/*.cpp           ../common/*.cpp

HEADERS +=  *.h             ./parser/*.h             ./parser/sexp/*.h

CONFIG += plugin
debug:DEFINES += __DEBUG__
QMAKE_LFLAGS_DEBUG += -shared -W
QMAKE_LFLAGS_RELEASE += -shared -W
DEFINES += YY_NO_UNISTD_H PERFT_FAST
DESTDIR = ../plugins/

QMAKE_CXXFLAGS += -std=c++0x
QMAKE_CXXFLAGS_DEBUG += -std=c++0x

QT += opengl

win32: {
CONFIG += static
} else {
QMAKE_CFLAGS_DEBUG += -rdynamic
QMAKE_CXXFLAGS_DEBUG += -rdynamic -g
QMAKE_LFLAGS_DEBUG += -rdynamic
LIBS += -lGLU
CONFIG += dll
}
