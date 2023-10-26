from PyQt5 import QtGui, QtCore
from PyQt5 import QtOpenGL

import OpenGL.GL as GL
from OpenGL import GLU

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
        GL.glEnable(GL.GL_DEPTH_TEST)  # enable depth testing

        self.initGeometry()

    def resizeGL(self, width, height):
        GL.glViewport(0, 0, width, height)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        aspect = width / float(height)

        GLU.gluPerspective(45.0, aspect, 1.0, 100.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def paintGL(self):
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

        GL.glPushMatrix()

        GL.glTranslate(0.0, 0.0, -25.0)
        GL.glScale(10.0, 10.0, 10.0)
        GL.glRotate(self.rotX, 1.0, 0.0, 0.0)
        GL.glRotate(self.rotY, 0.0, 1.0, 0.0)
        GL.glRotate(self.rotZ, 0.0, 0.0, 1.0)
        GL.glTranslate(-0.5, -0.5, -0.5)

        GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
        GL.glEnableClientState(GL.GL_COLOR_ARRAY)

        GL.glVertexPointer(3, GL.GL_FLOAT, 0, self.vertVBO)
        GL.glColorPointer(3, GL.GL_FLOAT, 0, self.colorVBO)

        GL.glDrawElements(GL.GL_QUADS, len(self.cubeIdxArray), GL.GL_UNSIGNED_INT, self.cubeIdxArray)

        GL.glDisableClientState(GL.GL_VERTEX_ARRAY)
        GL.glDisableClientState(GL.GL_COLOR_ARRAY)

        GL.glPopMatrix()

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
