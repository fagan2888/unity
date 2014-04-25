#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import app.clock as clock

__clock__   = None
__windows__ = []


def run(default_clock=None, framerate=0):
    """ Run the main loop """
    global __clock__

    if default_clock is None:
        __clock__ = clock.get_default()
    else:
        __clock__ = default_clock
    __clock__.set_fps_limit(framerate)

    # Initialize timers for all windows
    for window in backend.windows():
        window._clock = __clock__

        # Start timers
        for i in range(len(window._timer_stack)):
            handler, interval = window._timer_stack[i]
            __clock__.schedule_interval(handler, interval)

        # Dispatch init event
        window.dispatch_event('on_init')

    # Run until no more window
    count = len(backend.windows())
    while count:
        count = backend.process(__clock__.tick())



if __name__ == '__main__':
    import sys
    import argparse
    import OpenGL.GL as gl

    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", "-b", default="glfw",
                        choices=['glfw', 'pyglet', 'osxglut', 'sdl', 'sdl2', 'pyside'],
                        help="Backend to use, one of ")
    parser.add_argument("--framerate", "-f", default=60, type=int,
                        help="Framerate in frames/second")
    args = parser.parse_args()

    name = "app.backends.backend_" + args.backend
    __import__(name)
    backend = sys.modules[name]


    window = backend.Window()

    @window.event
    def on_init():
        print 'Initialization'

    @window.event
    def on_draw():
        gl.glClearColor(1,1,1,1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT )

    @window.timer(1.0)
    def timer(elapsed):
        print "FPS:", __clock__.get_fps()
        print 'Timed event 1 (%.3f second(s) elapsed)' % elapsed

    @window.event
    def on_resize(width,height):
        print 'Resized (width=%d, height=%d)' % (width,height)

    # @window.event
    # def on_idle(dt):
    #     print 'Idle event', dt

    @window.event
    def on_character(character):
        print 'Character entered(character=%s)'% (character)

    @window.event
    def on_key_press(symbol, modifiers):
        print 'Key pressed (symbol=%s, modifiers=%s)'% (symbol,modifiers)

    @window.event
    def on_key_release(symbol, modifiers):
        print 'Key released (symbol=%s, modifiers=%s)'% (symbol,modifiers)

    @window.event
    def on_mouse_press(x, y, button):
        print 'Mouse button pressed (x=%.1f, y=%.1f, button=%d)' % (x,y,button)

    @window.event
    def on_mouse_release(x, y, button):
        print 'Mouse button released (x=%.1f, y=%.1f, button=%d)' % (x,y,button)

    @window.event
    def on_mouse_motion(x, y, dx, dy):
        print 'Mouse motion (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f)' % (x,y,dx,dy)

    @window.event
    def on_mouse_drag(x, y, dx, dy, button):
        print 'Mouse drag (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f, button=%d)' % (x,y,dx,dy,button)

    @window.event
    def on_mouse_scroll(x, y, dx, dy):
        print 'Mouse scroll (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f)' % (x,y,dx,dy)


    # These two one cannot have multiple windows
    if backend.__name__ not in ['SDL', 'OSX GLUT']:

        window = backend.Window()
        @window.event
        def on_draw():
            gl.glClearColor(0,0,0,1)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT )

        @window.timer(1.0)
        def timer(elapsed):
            print 'Timed event 2 (%.3f second(s) elapsed)' % elapsed

        @window.event
        def on_mouse_motion(x, y, dx, dy):
            print 'Mouse motion (x=%.1f, y=%.1f, dx=%.1f, dy=%.1f)' % (x,y,dx,dy)

    run(framerate=args.framerate)
