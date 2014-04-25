# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
import os, sys, ctypes
from .. window import window
from .. import log, clock, configuration


# Backend name
__name__ = "SDL2"

# Backend version (if available)
__version__ = ""

# Whether the framework has been initialized
__initialized__ = False

# Active windows
__windows__ = {}

# Default clock
__clock__ = None


# --------------------------------------------------------------- init/exit ---
def __init__():
    global __initialized__
    if not __initialized__:
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
    __initialized__ = True

def __exit__():
    global __initialized__
    sdl2.SDL_Quit()
    __initialized__ = False


# ------------------------------------------------------------ availability ---
try:
    import sdl2
    if not __initialized__:
        __init__()
    availability = True
    __version__ = ("%d.%d.%d") % sdl2.version_info[:3]
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
def set_configuration(configuration):
    """ Set gl configuration """

    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_RED_SIZE, configuration.red_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_GREEN_SIZE, configuration.green_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_BLUE_SIZE, configuration.blue_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_ALPHA_SIZE, configuration.alpha_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_DEPTH_SIZE, configuration.depth_size)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_STENCIL_SIZE, configuration.stencil_size)
    if configuration.samples:
        sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1)
        sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_MULTISAMPLESAMPLES, configuration.samples)
    else:
        sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_MULTISAMPLEBUFFERS, 0)
        sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_MULTISAMPLESAMPLES, 0)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_STEREO, configuration.stereo)
    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_FRAMEBUFFER_SRGB_CAPABLE, configuration.srgb)
#    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_CONFIGURATION_MAJOR_VERSION,
#                              configuration.major_version)
#    sdl2.SDL_GL_SetAttribute( sdl2.SDL_GL_CONFIGURATION_MINOR_VERSION,
#                              configuration.minor_version)
#    if configuration.profile == "core":
#        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONFIGURATION_PROFILE_MASK,
#                                 sdl2.SDL_GL_CONFIGURATION_PROFILE_CORE)
#    elif configuration.profile == "compatibility":
#        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONFIGURATION_PROFILE_MASK,
#                                 sdl2.SDL_GL_CONFIGURATION_PROFILE_COMPATIBILITY)
#    elif configuration.profile == "es":
#        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_CONFIGURATION_PROFILE_MASK,
#                                 sdl2.SDL_GL_CONFIGURATION_PROFILE_ES)



# ------------------------------------------------------------------ Window ---
class Window(window.Window):
    """ """

    def __init__( self, width=256, height=256, title=None, visible=True,
                  decoration=True, fullscreen=False, config=None, context=None):
        """ """

        window.Window.__init__(self, width, height, title, visible,
                               decoration, fullscreen, config, context)
        if config is None:
            config = configuration.Configuration()
        set_configuration(config)

        flags  = sdl2.SDL_WINDOW_SHOWN
        flags |= sdl2.SDL_WINDOW_ALLOW_HIGHDPI
        flags |= sdl2.SDL_WINDOW_RESIZABLE
        flags |= sdl2.SDL_WINDOW_OPENGL
        if visible:
            flags |= sdl2.SDL_WINDOW_SHOWN
        else:
            flags |= SDL_WINDOW_HIDDEN
        if not decoration:
            flags |= sdl2.SDL_WINDOW_BORDERLESS

        self._native_window = sdl2.SDL_CreateWindow(self._title,
                                                    sdl2.SDL_WINDOWPOS_UNDEFINED,
                                                    sdl2.SDL_WINDOWPOS_UNDEFINED,
                                                    width, height, flags)
        self._native_context = sdl2.SDL_GL_CreateContext(self._native_window)
        self._native_id = sdl2.SDL_GetWindowID(self._native_window)

        sdl2.SDL_GL_SetSwapInterval(0)

        __windows__[self._native_id] = self


    def process_event(self, event):


        if event.type == sdl2.SDL_WINDOWEVENT:

            if event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED:
                width = event.window.data1
                height = event.window.data2
                self.dispatch_event('on_resize', width, height)
            elif event.window.event == sdl2.SDL_WINDOWEVENT_SHOWN:
                self.dispatch_event('on_show')
            elif event.window.event == sdl2.SDL_WINDOWEVENT_HIDDEN:
                self.dispatch_event('on_hide')
            elif event.window.event == sdl2.SDL_WINDOWEVENT_ENTER:
                self.dispatch_event('on_enter')
            elif event.window.event == sdl2.SDL_WINDOWEVENT_LEAVE:
                self.dispatch_event('on_leave')
            #elif event.window.event == sdl2.SDL_WINDOWEVENT_MOVED:
            #    self.dispatch_event('on_move')
            elif event.window.event == sdl2.SDL_WINDOWEVENT_CLOSE:
                self.close()

        elif event.type == sdl2.SDL_QUIT:
            self.close()

        elif event.type == sdl2.SDL_MOUSEMOTION:
            x = event.motion.x
            y = event.motion.y
            buttons = event.motion.state
            dx = x - self._mouse_x
            dy = y - self._mouse_y
            self._mouse_x = x
            self._mouse_y = y
            if buttons & sdl2.SDL_BUTTON_LMASK:
                self.dispatch_event("on_mouse_drag", x, y, dx, dy, window.mouse.LEFT)
            elif buttons & sdl2.SDL_BUTTON_MMASK:
                self.dispatch_event("on_mouse_drag", x, y, dx, dy, window.mouse.MIDDLE)
            elif buttons & sdl2.SDL_BUTTON_RMASK:
                self.dispatch_event("on_mouse_drag", x, y, dx, dy, window.mouse.RIGHT)
            else:
                self.dispatch_event("on_mouse_motion", x, y, dx, dy)

        elif event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            x = event.button.x
            y = event.button.y
            button = event.button.button
            self._mouse_x = x
            self._mouse_y = y
            if button == sdl2.SDL_BUTTON_LEFT:
                self.dispatch_event("on_mouse_press", x, y, window.mouse.LEFT)
            elif button == sdl2.SDL_BUTTON_MIDDLE:
                self.dispatch_event("on_mouse_press", x, y, window.mouse.MIDDLE)
            elif button == sdl2.SDL_BUTTON_RIGHT:
                self.dispatch_event("on_mouse_press", x, y, window.mouse.RIGHT)

        elif event.type == sdl2.SDL_MOUSEBUTTONUP:
            x = event.button.x
            y = event.button.y
            button = event.button.button
            self._mouse_x = x
            self._mouse_y = y
            if button == sdl2.SDL_BUTTON_LEFT:
                self.dispatch_event("on_mouse_release", x, y, window.mouse.LEFT)
            elif button == sdl2.SDL_BUTTON_MIDDLE:
                self.dispatch_event("on_mouse_release", x, y, window.mouse.MIDDLE)
            elif button == sdl2.SDL_BUTTON_RIGHT:
                self.dispatch_event("on_mouse_release", x, y, window.mouse.RIGHT)

        elif event.type == sdl2.SDL_MOUSEWHEEL:
            offset_x = event.wheel.x
            offset_y = event.wheel.y
            self.dispatch_event("on_mouse_scroll",
                                self._mouse_x, self._mouse_y, offset_x, offset_y)


        # elif event.type == pygame.KEYUP:
        #     modifiers = self._modifiers_translate(event.mod)
        #     symbol = self._keyboard_translate(event.key)
        #     self._on_key_press(symbol, modifiers)

        # elif event.type == pygame.KEYDOWN:
        #     modifiers = self._modifiers_translate(event.mod)
        #     symbol = self._keyboard_translate(event.key)
        #     self._on_key_release(symbol, modifiers)


    def _modifiers_translate( self, modifiers ):
        _modifiers = 0
        if modifiers & (pygame.K_LSHIFT | pygame.K_RSHIFT):
            _modifiers |=  window.key.MOD_SHIFT
        if modifiers & (pygame.K_LCTRL | pygame.K_RCTRL):
            _modifiers |=  window.key.MOD_CTRL
        if modifiers & (pygame.K_LALT | pygame.K_RALT):
            _modifiers |=  window.key.MOD_ALT
        return _modifiers

    def _keyboard_translate(self, code):
        ascii = code
        if (0x020 <= ascii <= 0x040) or (0x05b <= ascii <= 0x07e):
            return ascii
        elif ascii < 0x020:
            if   ascii == 0x008: return window.key.BACKSPACE
            elif ascii == 0x009: return window.key.TAB
            elif ascii == 0x00A: return window.key.LINEFEED
            elif ascii == 0x00C: return window.key.CLEAR
            elif ascii == 0x00D: return window.key.RETURN
            elif ascii == 0x018: return window.key.CANCEL
            elif ascii == 0x01B: return window.key.ESCAPE
        elif code==pygame.K_F1:       return window.key.F1
        elif code==pygame.K_F2:       return window.key.F2
        elif code==pygame.K_F3:       return window.key.F3
        elif code==pygame.K_F4:       return window.key.F4
        elif code==pygame.K_F5:       return window.key.F5
        elif code==pygame.K_F6:       return window.key.F6
        elif code==pygame.K_F7:       return window.key.F7
        elif code==pygame.K_F8:       return window.key.F8
        elif code==pygame.K_F9:       return window.key.F9
        elif code==pygame.K_F10:      return window.key.F10
        elif code==pygame.K_F11:      return window.key.F11
        elif code==pygame.K_F12:      return window.key.F12
        elif code==pygame.K_LEFT:     return window.key.LEFT
        elif code==pygame.K_UP:       return window.key.UP
        elif code==pygame.K_RIGHT:    return window.key.RIGHT
        elif code==pygame.K_DOWN:     return window.key.DOWN
        elif code==pygame.K_PAGE_UP:  return window.key.PAGEUP
        elif code==pygame.K_PAGE_DOWN:return window.key.PAGEDOWN
        elif code==pygame.K_HOME:     return window.key.HOME
        elif code==pygame.K_END:      return window.key.END
        elif code==pygame.K_INSERT:   return window.key.INSERT


    def show(self):
        sdl2.SDL_ShowWindow(self._native_window)
        self.dispatch_event('on_show')

    def hide(self):
        sdl2.SDL_HideWindow(self._native_window)
        self.dispatch_event('on_hide')

    def close(self):

        del __windows__[self._native_id]
        for i in range(len(self._timer_stack)):
            handler, interval = self._timer_stack[i]
            self._clock.unschedule(handler)
        sdl2.SDL_DestroyWindow(self._native_window)
        self.dispatch_event('on_close')

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

    def swap(self):
        sdl2.SDL_GL_SwapWindow(self._native_window)

    def activate(self):
        sdl2.SDL_GL_MakeCurrent(self._native_window, self._native_context)



# ----------------------------------------------------------------- windows ---
def windows():
    return __windows__.values()


# ----------------------------------------------------------------- process ---
def process(dt):

    # Poll for and process events
    event = sdl2.SDL_Event()
    while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
        win_id = event.window.windowID
        if win_id in __windows__.keys():
            win = __windows__[win_id]
            win.process_event(event)

    for window in windows():
        # Make window active
        window.activate()

        # Dispatch the main draw event
        window.dispatch_event('on_draw')

        # Dispatch the idle event
        window.dispatch_event('on_idle', dt)

        # Swap buffers
        window.swap()

    return len(__windows__.values())
