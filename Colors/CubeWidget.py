from PyQt5 import QtGui, QtCore
from PyQt5 import QtOpenGL

import OpenGL.GL as gl
from OpenGL import GLU
from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

from OpenGL.arrays import vbo
import numpy as np


class CubeWidget(QWidget):
    def __init__(self, parent=None):
        super(CubeWidget, self).__init__(parent)
        self.glWidget = GLWidget(self)
        self.initGUI()

        self.setFixedSize(300, 300)

        self.isUp = False

        timer = QtCore.QTimer(self)
        timer.setInterval(20)  # period, in milliseconds
        timer.timeout.connect(self.glWidget.updateGL)
        timer.start()

    def initGUI(self):
        gui_layout = QVBoxLayout()

        self.setLayout(gui_layout)

        gui_layout.addWidget(self.glWidget)

        buttonUp = QPushButton("Up/Down")
        buttonUp.clicked.connect(self.rotateUp)
        gui_layout.addWidget(buttonUp)

        buttonRight = QPushButton("Rotate")
        buttonRight.clicked.connect(self.rotateRight)
        gui_layout.addWidget(buttonRight)

    def rotateUp(self):
        newRot = (self.glWidget.rotX + 180) % 360
        self.glWidget.rotX = newRot
        if self.isUp:
            self.isUp = False
            newRot = (self.glWidget.rotY - 30) % 360
        else:
            self.isUp = True
            newRot = (self.glWidget.rotY + 30) % 360
        self.glWidget.rotY = newRot



    def rotateRight(self):
        newRot = (self.glWidget.rotY + 90) % 360
        self.glWidget.rotY = newRot

class GLWidget(QtOpenGL.QGLWidget):
    def __init__(self, parent=None):
        self.parent = parent
        QtOpenGL.QGLWidget.__init__(self, parent)

        self.rotX = 30.0
        self.rotY = 30.0
        self.rotZ = 0.0

    def initializeGL(self):
        self.qglClearColor(QtGui.QColor(0, 0, 0))  # initialize the screen to blue
        gl.glEnable(gl.GL_DEPTH_TEST)  # enable depth testing

        self.initGeometry()

    def resizeGL(self, width, height):
        gl.glViewport(0, 0, width, height)
        gl.glMatrixMode(gl.GL_PROJECTION)
        gl.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        gl.glMatrixMode(gl.GL_MODELVIEW)

    def paintGL(self):
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        gl.glPushMatrix()

        gl.glTranslate(0.0, 0.0, -25.0)
        gl.glScale(10.0, 10.0, 10.0)
        gl.glRotate(self.rotX, 1.0, 0.0, 0.0)
        gl.glRotate(self.rotY, 0.0, 1.0, 0.0)
        gl.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        gl.glTranslate(-0.5, -0.5, -0.5)

        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        gl.glEnableClientState(gl.GL_COLOR_ARRAY)

        gl.glVertexPointer(3, gl.GL_FLOAT, 0, self.vertVBO)
        gl.glColorPointer(3, gl.GL_FLOAT, 0, self.colorVBO)

        gl.glDrawElements(gl.GL_QUADS, len(self.cubeIdxArray), gl.GL_UNSIGNED_INT, self.cubeIdxArray)

        gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
        gl.glDisableClientState(gl.GL_COLOR_ARRAY)

        gl.glPopMatrix()

    def initGeometry(self):
        self.cubeVtxArray = np.array(
            [[0.0, 0.0, 0.0],
             [1.0, 0.0, 0.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        self.vertVBO = vbo.VBO(np.reshape(self.cubeVtxArray,
                                          (1, -1)).astype(np.float32))
        self.vertVBO.bind()

        self.cubeClrArray = np.array(
            [[1.0, 1.0, 1.0],
             [1.0, 1.0, 1.0],
             [1.0, 1.0, 0.0],
             [0.0, 1.0, 0.0],
             [0.0, 0.0, 1.0],
             [1.0, 0.0, 1.0],
             [1.0, 1.0, 1.0],
             [0.0, 1.0, 1.0]])
        self.colorVBO = vbo.VBO(np.reshape(self.cubeClrArray,
                                           (1, -1)).astype(np.float32))

        self.cubeIdxArray = np.array(
            [0, 1, 2, 3,
             3, 2, 6, 7,
             1, 0, 4, 5,
             2, 1, 5, 6,
             0, 3, 7, 4,
             7, 6, 5, 4])

    def setRotX(self, val):
        self.rotX = np.pi * val

    def setRotY(self, val):
        self.rotY = np.pi * val

    def setRotZ(self, val):
        self.rotZ = np.pi * val