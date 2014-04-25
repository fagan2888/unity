# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import os, sys
from .. window import window
from .. import log, clock, configuration


# Backend name
__name__ = "PYSIDE"

# Backend version (if available)
__version__ = ""

# Whether the framework has been initialized
__initialized__ = False

# Active windows
__windows__ = []

# Default clock
__clock__ = None

# GL Format
__glformat__ = None


# --------------------------------------------------------------- init/exit ---
def __init__():
    global __initialized__
    __app__ = QtGui.QApplication.instance()
    if __app__ is None:
        __app__ = QtGui.QApplication(sys.argv)
    __initialized__ = True

def __exit__():
    global __initialized__
    __initialized__ = False


# ------------------------------------------------------------ availability ---
try:
    from PySide import QtGui, QtCore, QtOpenGL
    if not __initialized__:
        __init__()
    availability = True
    __version__ = QtCore.__version__

    __mouse_map__ = { 0: window.mouse.LEFT,
                      1: window.mouse.MIDDLE,
                      2: window.mouse.RIGHT }

    __key_map__ = { QtCore.Qt.Key_Left:      window.key.LEFT,
                    QtCore.Qt.Key_Up:        window.key.UP,
                    QtCore.Qt.Key_Right:     window.key.RIGHT,
                    QtCore.Qt.Key_Down:      window.key.DOWN,
                    QtCore.Qt.Key_PageUp:    window.key.PAGEUP,
                    QtCore.Qt.Key_PageDown:  window.key.PAGEDOWN,
                    QtCore.Qt.Key_Insert:    window.key.INSERT,
                    QtCore.Qt.Key_Delete:    window.key.DELETE,
                    QtCore.Qt.Key_Home:      window.key.HOME,
                    QtCore.Qt.Key_End:       window.key.END,
                    QtCore.Qt.Key_Escape:    window.key.ESCAPE,
                    QtCore.Qt.Key_Backspace: window.key.BACKSPACE,
                    QtCore.Qt.Key_F1:        window.key.F1,
                    QtCore.Qt.Key_F2:        window.key.F2,
                    QtCore.Qt.Key_F3:        window.key.F3,
                    QtCore.Qt.Key_F4:        window.key.F4,
                    QtCore.Qt.Key_F5:        window.key.F5,
                    QtCore.Qt.Key_F6:        window.key.F6,
                    QtCore.Qt.Key_F7:        window.key.F7,
                    QtCore.Qt.Key_F8:        window.key.F8,
                    QtCore.Qt.Key_F9:        window.key.F9,
                    QtCore.Qt.Key_F10:       window.key.F10,
                    QtCore.Qt.Key_F11:       window.key.F11,
                    QtCore.Qt.Key_F12:       window.key.F12,
                    QtCore.Qt.Key_Space:     window.key.SPACE,
                    QtCore.Qt.Key_Enter:     window.key.ENTER,
                    QtCore.Qt.Key_Return:    window.key.ENTER,
                    QtCore.Qt.Key_Tab:       window.key.TAB }


except ImportError:
    availability = False
    __version__ = None


# -------------------------------------------------------------- capability ---
capability = {
    "Window position get/set" : True,
    "Window size get/set"     : True,
    "Multiple windows"        : True,
    "Mouse scroll events"     : True,
    "Non-decorated window"    : True,
    "Non-sizeable window"     : True,
    "Fullscreen mode"         : True,
    "Unicode processing"      : True,
    "Set GL version"          : True,
    "Set GL profile"          : True,
    "Share GL context"        : True,
}


# ------------------------------------------------------- set_configuration ---
def set_configuration(config):
    global __glformat__

    __glformat__ = QtOpenGL.QGLFormat()
    __glformat__.setSwapInterval(0)
    __glformat__.setRedBufferSize(config.red_size)
    __glformat__.setGreenBufferSize(config.green_size)
    __glformat__.setBlueBufferSize(config.blue_size)
    __glformat__.setAlphaBufferSize(config.alpha_size)
    __glformat__.setAccum(False)
    __glformat__.setRgba(True)

    if config.double_buffer:
        __glformat__.setDoubleBuffer(True)
    else:
        __glformat__.setDoubleBuffer(False)

    if config.depth_size:
        __glformat__.setDepth(True)
        __glformat__.setDepthBufferSize(config.depth_size)
    else:
        __glformat__.setDepth(False)
        __glformat__.setDepthBufferSize(0)

    if config.stencil_size:
        __glformat__.setStencil(True)
        __glformat__.setStencilBufferSize(config.stencil_size)
    else:
        __glformat__.setStencil(False)
        __glformat__.setStencilBufferSize(0)

    if config.samples:
        __glformat__.setSampleBuffers(True)
        __glformat__.setSamples(config.samples)
    else:
        __glformat__.setSampleBuffers(False)
        __glformat__.setSamples(0)
    __glformat__.setStereo(config.stereo)

    # __glformat__.setVersion(config.major_version, config.minor_version)
    # __glformat__.setProfile(QGLFormat::NoProfile)
    # __glformat__.setProfile(QGLFormat::CoreProfile)
    # __glformat__.setProfile(QGLFormat::CompatibilityProfile)


# ------------------------------------------------------------------ Window ---
class Window(window.Window):
    def __init__( self, width=256, height=256, title=None, visible=True,
                  decoration=True, fullscreen=False, config=None, context=None):

        window.Window.__init__(self, width, height, title, visible,
                               decoration, fullscreen, config, context)

        if config is None:
            config = configuration.Configuration()
        set_configuration(config)

        self._native_app = QtGui.QApplication.instance()
        if self._native_app is None:
            self._native_app = QtGui.QApplication(sys.argv)

        self._native_window = QtOpenGL.QGLWidget(__glformat__)
        self._native_window.resize(width, height)
        self._native_window.makeCurrent()
        self._native_window.setAutoBufferSwap(False)
        self._native_window.setMouseTracking(True)
        self._native_window.setWindowTitle(self._title)
        self._native_window.show()

        def paint_gl():
            self.dispatch_event("on_draw")
        self._native_window.paintGL = paint_gl

        def resize_gl(width, height):
            self.dispatch_event("on_resize", width, height)
        self._native_window.resizeGL = resize_gl

        def close_event(event):
            __windows__.remove(self)
            self.dispatch_event("on_close")
        self._native_window.closeEvent = close_event

        def mouse_press_event(event):
            x = event.pos().x()
            y = event.pos().y()
            button = __mouse_map__.get(event.button(), window.mouse.UNKNOWN)
            self._button = button
            self._mouse_x = x
            self._mouse_y = y
            self.dispatch_event("on_mouse_press", x, y, button)
        self._native_window.mousePressEvent = mouse_press_event

        def mouse_release_event(event):
            x = event.pos().x()
            y = event.pos().y()
            button = __mouse_map__.get(event.button(), window.mouse.UNKNOWN)
            self._button = window.mouse.NONE
            self._mouse_x = x
            self._mouse_y = y
            self.dispatch_event("on_mouse_release", x, y, button)
        self._native_window.mouseReleaseEvent = mouse_release_event

        def mouse_move_event(event):
            x = event.pos().x()
            y = event.pos().y()
            dx = x - self._mouse_x
            dy = y - self._mouse_y
            self._mouse_x = x
            self._mouse_y = y
            if self._button is not window.mouse.NONE:
                self.dispatch_event('on_mouse_drag', x, y, dx, dy, self._button)
            else:
                self.dispatch_event('on_mouse_motion', x, y, dx, dy)
        self._native_window.mouseMoveEvent = mouse_move_event

        def wheel_event(event):
            if event.orientation == QtCore.Qt.Horizontal:
                offset_x = event.delta()
                offset_y = 0
            else:
                offset_x = 0
                offset_y = event.delta()
            x = event.pos().x()
            y = event.pos().y()
            self.dispatch_event("on_mouse_scroll", x, y, offset_x, offset_y)

        self._native_window.wheelEvent = wheel_event

        def key_press_event(event):
            code = self._keyboard_translate(event.key())
            modifiers = self._modifiers_translate(event.modifiers())
            self.dispatch_event("on_key_press", code, modifiers)
            self.dispatch_event("on_character", event.text())
        self._native_window.keyPressEvent = key_press_event

        def key_release_event(event):
            code = self._keyboard_translate(event.key())
            modifiers = self._modifiers_translate(event.modifiers())
            self.dispatch_event("on_key_release", code, modifiers)
        self._native_window.keyReleaseEvent = key_release_event

        __windows__.append(self)

    def _keyboard_translate( self, code ):
        if code in __key_map__:
            return __key_map__[code]
        if 32 <= code <= 96 or code in [161,162]:
            return code
        return window.key.UNKNOWN

    def _modifiers_translate( self, modifiers ):
        _modifiers = 0
        if QtCore.Qt.ShiftModifier & modifiers:
            _modifiers |= window.key.SHIFT,
        if QtCore.Qt.ControlModifier & modifiers:
            _modifiers += window.key.CONTROL,
        if QtCore.Qt.AltModifier & modifiers:
            _modifiers += window.key.ALT,
        if QtCore.Qt.MetaModifier & modifiers:
            _modifiers += window.key.META,
        return _modifiers

    def _modifiers_translate( self, modifiers ):
        _modifiers = 0
        if QtCore.Qt.ShiftModifier & modifiers:
            _modifiers |= window.key.SHIFT,
        if QtCore.Qt.ControlModifier & modifiers:
            _modifiers += window.key.CONTROL,
        if QtCore.Qt.AltModifier & modifiers:
            _modifiers += window.key.ALT,
        if QtCore.Qt.MetaModifier & modifiers:
            _modifiers += window.key.META,
        return _modifiers

    def show(self):
        self._native_window.show()
        self.dispatch_event('on_show')

    def hide(self):
        self._native_window.hide()
        self.dispatch_event('on_hide')

    def set_title(self, title):
        self._native_window.setWindowTitle(self._title)
        self._title = title

    def get_title(self, title):
        return self._title

    def set_size(self, width, height):
        self._native_window.resize(width, height)
        self._width = self._native_window.geometry().width()
        self._height = self._native_window.geometry().height()

    def get_size(self):
        self._width = self._native_window.geometry().width()
        self._height = self._native_window.geometry().height()
        return self._width, self._height

    def set_position(self, x, y):
        self._native_window.move(x,y)
        self._x = self._native_window.geometry().x()
        self._y = self._native_window.geometry().y()

    def get_position(self):
        self._x = self._native_window.geometry().x()
        self._y = self._native_window.geometry().y()
        return self._x, self._y

    def swap(self):
        self._native_window.swapBuffers()

    def activate(self):
        self._native_window.makeCurrent()



# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__


# ----------------------------------------------------------------- process ---
def process(dt):

    for window in __windows__:
        # Poll for and process events
        window._native_app.processEvents()
        # window._native_app.flush()

    for window in __windows__:
        # Make window active
        window.activate()

        # Dispatch the main draw event
        window.dispatch_event('on_draw')

        # Dispatch the idle event
        window.dispatch_event('on_idle', dt)

        # Swap buffers
        window.swap()


    return len(__windows__)
