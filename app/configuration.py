# -*- coding: utf-8 -*-
# Copyright (c) 2014, Vispy Development Team.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.


# ----------------------------------------------------------- Configuration ---
class Configuration(object):
    """
    GL Configuration settings
    """

    def __init__(self):

        self._red_size            = 8
        self._green_size          = 8
        self._blue_size           = 8
        self._alpha_size          = 8

        self._double_buffer       = True
        self._depth_size          = 16
        self._stencil_size        = 0
        self._samples             = 0

        self._stereo              = False
        self._srgb                = False

        self._major_version       = 2
        self._minor_version       = 1
        self._profile             = "compatibility"


    # ---------------------------------------------------------------- repr ---
    def __repr__(self):
        s = ""
        s += "Color buffer size:     %d bit(s) (R:%d, G:%d, B:%d, A:%d)\n" % (
            self._red_size + self._green_size + self._blue_size + self._alpha_size,
            self._red_size,
            self._green_size,
            self._blue_size,
            self._alpha_size)
        s += "Depth buffer size:     %d bit(s)\n" % (self._depth_size)
        s += "Stencil buffer size:   %d bit(s)\n" % (self._stencil_size)
        s += "Double buffered:       %d\n" % (self._double_buffer)
        s += "Stereo mode:           %d\n" % (self._stereo)
        s += "sRGB mode:             %d\n" % (self._srgb)
        s += "Anti-aliasing samples: %d\n" % (self._samples)
        s += "GL Version:            %d.%d\n" % (self._major_version,
                                                 self._minor_version)
        s += "GL Profile:            %s" % (self._profile)
        return s



    # ------------------------------------------------------------ red size ---
    @property
    def red_size(self):
        """
        Minimum number of bits for the red channel of the color buffer.
        """
        return self._red_size


    # ---------------------------------------------------------- green size ---
    @property
    def green_size(self):
        """
        Minimum number of bits for the blue channel of the color buffer.
        """
        return self._green_size


    # ----------------------------------------------------------- blue size ---
    @property
    def blue_size(self):
        """
        Minimum number of bits for the green channel of the color buffer.
        """
        return self._blue_size


    # ---------------------------------------------------------- alpha size ---
    @property
    def alpha_size(self):
        """
        Minimum number of bits for the alpha channel of the color buffer.
        """
        return self._alpha_size


    # ------------------------------------------------------- double buffer ---
    @property
    def double_buffer(self):
        """
        Whether to use single or double buffered rendering.
        """
        return self._double_buffer


    # ---------------------------------------------------------- depth size ---
    @property
    def depth_size(self):
        """
        Minimum number of bits in the depth buffer.
        """
        return self._depth_size


    # -------------------------------------------------------- stencil size ---
    @property
    def stencil_size(self):
        """
        Minimum number of bits in the stencil buffer.
        """
        return self._stencil_size


    # -------------------------------------------------------------- stereo ---
    @property
    def stereo(self):
        """
        Whether the output is stereo.
        """
        return self._stereo


    # ------------------------------------------------------------- samples ---
    @property
    def samples(self):
        """
        Number of samples used around the current pixel for multisample
        anti-aliasing
        """
        return self._samples


    # ------------------------------------------------------- major version ---
    @property
    def major_version(self):
        """
        OpenGL context major version
        """
        return self._major_version


    # ------------------------------------------------------- minor version ---
    @property
    def minor_version(self):
        """
        OpenGL context minor version
        """
        return self._minor_version


    # ------------------------------------------------------------- profile ---
    @property
    def profile(self):
        """
        OpenGL profile
        """
        return self._profile


    # ---------------------------------------------------------------- srgb ---
    @property
    def srgb(self):
        """
        Whether to user sRGB capable visuals.
        """
        return self._srgb



# ---------------------------------------------------- gl_get_configuration ---
def gl_get_configuration():
    """
    Read gl configuration independently of backends.
    """

    import ctypes
    import OpenGL.GL as gl

    configuration =  Configuration()
    gl.glBindFramebuffer(gl.GL_FRAMEBUFFER, 0)
    value = ctypes.c_int()
    gl.glGetFramebufferAttachmentParameteriv(
        gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
        gl.GL_FRAMEBUFFER_ATTACHMENT_RED_SIZE, value )
    configuration._red_size = value.value

    gl.glGetFramebufferAttachmentParameteriv(
        gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
        gl.GL_FRAMEBUFFER_ATTACHMENT_GREEN_SIZE, value )
    configuration._green_size = value.value

    gl.glGetFramebufferAttachmentParameteriv(
        gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
        gl.GL_FRAMEBUFFER_ATTACHMENT_BLUE_SIZE, value )
    configuration._blue_size = value.value

    gl.glGetFramebufferAttachmentParameteriv(
        gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
        gl.GL_FRAMEBUFFER_ATTACHMENT_ALPHA_SIZE, value )
    configuration._alpha_size = value.value

    gl.glGetFramebufferAttachmentParameteriv(
        gl.GL_FRAMEBUFFER, gl.GL_DEPTH,
        gl.GL_FRAMEBUFFER_ATTACHMENT_DEPTH_SIZE, value )
    configuration._depth_size = value.value

    gl.glGetFramebufferAttachmentParameteriv(
        gl.GL_FRAMEBUFFER, gl.GL_STENCIL,
        gl.GL_FRAMEBUFFER_ATTACHMENT_STENCIL_SIZE, value )
    configuration._stencil_size = value.value

    gl.glGetFramebufferAttachmentParameteriv(
        gl.GL_FRAMEBUFFER, gl.GL_FRONT_LEFT,
        gl.GL_FRAMEBUFFER_ATTACHMENT_COLOR_ENCODING, value )
    if value.value == gl.GL_LINEAR:
        configuration._srgb = False
    elif value.value == gl.GL_SRGB:
        configuration._srgb = True

    configuration._stereo        = gl.glGetInteger(gl.GL_STEREO)
    configuration._double_buffer = gl.glGetInteger(gl.GL_DOUBLEBUFFER)
    configuration._samples       = gl.glGetInteger(gl.GL_SAMPLES)

    # Dumb parsing of the GL_VERSION string
    version = gl.glGetString(gl.GL_VERSION)
    version = version.split(" ")[0]
    major,minor = version.split('.')
    configuration._major_version = int(major)
    configuration._minor_version = int(minor)

    return configuration
