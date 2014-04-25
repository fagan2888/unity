#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# glumpy is an OpenGL framework for the fast visualization of numpy arrays.
# Copyright (C) 2009-2011  Nicolas P. Rougier. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY NICOLAS P. ROUGIER ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL NICOLAS P. ROUGIER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are
# those of the authors and should not be interpreted as representing official
# policies, either expressed or implied, of Nicolas P. Rougier.
# -----------------------------------------------------------------------------
import sys
import key
import event
import mouse
from .. import log


class Window(event.EventDispatcher):
    '''Platform independent window.

    The content area of a window is filled entirely with an OpenGL viewport.
    Applications have no access to operating system widgets or controls; all
    rendering must be done via OpenGL.

    Windows may appear as floating regions or can be set to fill an entire
    screen (fullscreen).  When floating, windows may appear borderless or
    decorated with a platform-specific frame (including, for example, the
    title bar, minimize and close buttons, resize handles, and so on).

    While it is possible to set the location of a window, it is recommended
    that applications allow the platform to place it according to local
    conventions.  This will ensure it is not obscured by other windows,
    and appears on an appropriate screen for the user.

    It is the responsability of the window backend to dispatch the following
    events when necessary:

    Keyboard::

      def on_key_press(symbol, modifiers):
          'A key on the keyboard was pressed.'
          pass

      def on_key_release(symbol, modifiers):
          'A key on the keyboard was released.'
          pass


    Mouse::

      def on_mouse_press(self, x, y, button):
          'A mouse button was pressed.'
          pass

      def on_mouse_release(self, x, y, button):
          'A mouse button was released.'
          pass

      def on_mouse_motion(x, y, dx, dy):
          'The mouse was moved with no buttons held down.'
          pass

      def on_mouse_drag(x, y, dx, dy, buttons):
          'The mouse was moved with some buttons pressed.'
          pass

      def on_mouse_scroll(self, dx, dy):
          'The mouse wheel was scrolled by (dx,dy).'
          pass


    Window::

      def on_init(self):
          'The window has just initialized iself.'
          pass

      def on_show(self):
          'The window was shown.'
          pass

      def on_hide(self):
          'The window was hidden.'
          pass

      def on_close(self,):
          'The user closed the window.'
          pass

      def on_resize(self, width, height):
          'The window was resized to (width,height)'
          pass

      def on_draw(self):
          'The window contents must be redrawn.'
          pass

      def on_idle(self):
          'The window is inactive.'
          pass
    '''

    def __init__( self, width=256, height=256, title=None, visible=True,
                  decoration=True, fullscreen=False, config=None, context=None):
        ''' '''
        self._mouse_x = 0
        self._mouse_y = 0
        self._button = 0
        self._x = 0
        self._y = 0
        self._title = title or sys.argv[0]
        self._width = width
        self._height = height
        self._visible = visible
        self._fullscreen = fullscreen
        self._decoration = decoration
        self._clock = None
        self._timer_stack = []
        self._timer_date = []


    def show(self):
        log.warn('%s backend cannot show window' % __name__)

    def hide(self):
        log.warn('%s backend cannot hide window' % __name__)

    def close(self):
        log.warn('%s backend cannot close window' % __name__)

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

    def timer( self, fps ):
        '''Function decorator for timed handlers.

        :Parameters:

            ``fps``: int
                Frames per second

        Usage::

            win = window.Window()
            @win.timer(60)
            def timer(dt):
                do_something ...
        '''

        def decorator(func):
            self._timer_stack.append((func, fps))
            self._timer_date.append(0)
            return func
        return decorator


Window.register_event_type('on_character')
Window.register_event_type('on_key_press')
Window.register_event_type('on_key_release')
Window.register_event_type('on_mouse_motion')
Window.register_event_type('on_mouse_drag')
Window.register_event_type('on_mouse_press')
Window.register_event_type('on_mouse_release')
Window.register_event_type('on_mouse_scroll')
Window.register_event_type('on_enter')
Window.register_event_type('on_leave')
Window.register_event_type('on_init')
Window.register_event_type('on_show')
Window.register_event_type('on_hide')
Window.register_event_type('on_close')
Window.register_event_type('on_resize')
Window.register_event_type('on_draw')
Window.register_event_type('on_idle')
