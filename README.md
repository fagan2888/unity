Experimental app framework for vispy
====================================


This is a tentative app framework for the vispy project.

This app offers a unified view on different toolkit (glut, glfw, sdl, sdl2,
glut, qt, pyglet), using the pyglet event system.

Test with:

$ ./test-backend.py --framerate 60 --backend glfw
$ ./test-backend.py --framerate 0 --backend sdl2

for example
