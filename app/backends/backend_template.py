# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import os, sys
from .. window import window
from .. import log, clock, configuration


# Backend name
__name__ = "Template"

# Backend version (if available)
__version__ = ""

# Whether the framework has been initialized
__initialized__ = False

# Active windows
__windows__ = []

# Default clock
__clock__ = None


# --------------------------------------------------------------- init/exit ---
def __init__():
    global __initialized__
    __initialized__ = True

def __exit__():
    global __initialized__
    __initialized__ = False


# ------------------------------------------------------------ availability ---
try:
    import ToolKit # Replace with actual toolkit
    availability = True
    __version__ = ""
    __key_map__   = { }
    __mouse_map__ = { }

except ImportError:
    availability = False
    __version__ = None


# -------------------------------------------------------------- capability ---
capability = {
    "Window position get/set" : False,
    "Window size get/set"     : False,
    "Multiple windows"        : False,
    "Mouse scroll events"     : False,
    "Non-decorated window"    : False,
    "Non-sizeable window"     : False,
    "Fullscreen mode"         : False,
    "Unicode processing"      : False,
    "Set GL version"          : False,
    "Set GL profile"          : False,
    "Share GL context"        : False,
}



# ------------------------------------------------------- set_configuration ---
def set_configuration(configuration):
    # Put GL initialization here (depth buffer size, etc.)
    pass



# ------------------------------------------------------------------ Window ---
class Window(event.EventDispatcher):


    def __init__( self, width=256, height=256, title=None,
                  visible=True, decoration=True, fullscreen=False,
                  sizeable=True, config=None, context=None):

        # Create the native window here
        # Each on the events below must be called at some point
        pass


    def _on_init(self):
        self.dispatch_event('on_init')

    def _on_show(self):
        self.dispatch_event('on_show')

    def _on_hide(self):
        self.dispatch_event('on_hide')

    def _on_close(self):
        self.dispatch_event('on_close')

    def _on_resize(self, width, height):
        self.dispatch_event('on_resize', width, height)

    def _on_mouse_release(self, x, y, button):
        self.dispatch_event('on_mouse_release', x, y, button)

    def _on_mouse_press(self, x, y, button):
        self.dispatch_event('on_mouse_press', x, y, button)

    def _on_mouse_motion(self, x, y, dx, dy):
        self.dispatch_event('on_mouse_motion', x, y, dx, dy)

    def _on_mouse_drag(self, x, y, dx, dy, button):
        self.dispatch_event('on_mouse_drag', x, y, dx, dy, button)

    def _on_scroll(self, x, y, xoffset, yoffset):
        self.dispatch_event('on_mouse_scroll', x, y, xoffset, yoffset)

    def _on_key_press(self, symbol, modifiers):
        self.dispatch_event('on_key_press', symbol, modifiers)

    def _on_key_release(self, symbol, modifiers):
        self.dispatch_event('on_key_release', symbol, modifiers)

    def _on_character(self, character):
        self.dispatch_event('on_character', u"%c" % character)


    def show(self):
        log.warn('%s backend cannot show window' % __name__)

    def hide(self):
        log.warn('%s backend cannot hide window' % __name__)

    def close(self):
        __windows__.remove(self)

    def set_title(self, title):
        log.warn('%s backend cannot set window title' % __name__)

    def get_title(self):
        log.warn('%s backend cannot get window title' % __name__)

    def set_size(self, width, height):
        log.warn('%s backend cannot set window size' % __name__)

    def get_size(self):
        log.warn('%s backend cannot get window size' % __name__)

    def set_position(self, x, y):
        log.warn('%s backend cannot set window position' % __name__)

    def get_position(self):
        log.warn('%s backend cannot get position' % __name__)

    def swap(self):
        log.warn('%s backend cannot swap buffers' % __name__)

    def activate(self):
        log.warn('%s backend cannot make window active' % __name__)


# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__


# ----------------------------------------------------------------- process ---
def process(dt):

    # Poll for and process events
    # -> Add toolkit specific code here to process events
    # -> Must always exit

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
