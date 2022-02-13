# This Python file uses the following encoding: utf-8
from pynput import mouse
import sys, os, time, random, math
from PyQt5.QtWidgets import QApplication, QMainWindow
from Animation import Animation
from PyQt5 import *
# from PyQt5 import QtCore, QtGui, QtMultimedia, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtCore import QEvent, Qt, QTimer
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget
import numpy as np
from copy import deepcopy

from Cope import *
# import pyautogui as ag
from pyautogui import position as mouseCoord
from globals import *

from os.path import join, dirname

DIR = dirname(__file__)

class AlwaysInFrontCharacter(QLabel):
    closeEnoughToMouse = 20
    def __init__(self, size,
                       framesDirectory,
                       frameSpeed=400, # In milliseconds
                       moveSpeed=20,   # In pixels - sorta
                       minSleepCycles = 5,
                       maxSleepCycles = 100
                ):
        self.size = size
        QLabel.__init__(self)
        self.setBorderless()
        self.animations = ZerosDict(self.setAnimations(self.loadPixmaps(framesDirectory)))

        self.mouseListener = mouse.Listener(on_click=self.onMouseClicked, on_move=self.onMouseMoved, on_scroll=self.onMouseScrolled)

        self.frameSpeed = frameSpeed
        self.moveSpeed = moveSpeed

        self.mission = self.idle

        self.runningAnimName = 'idle'
        self.runningAnim = self.animations['idle']
        self.runningAnim.play()

        self.lastClickPos = mouseCoord()

    def onMouseClicked(self, x, y, button, pressed):
        if pressed:
            debug(button)
            self.lastClickPos = (x, y)

    def onMouseMoved(self, x, y):
        pass

    def onMouseScrolled(self, x, y, dx, dy):
        pass

    def loadPixmaps(self, dir):
        """ Load all the frames """
        pixmaps = {}
        for frame in os.listdir(dir):
            pixmaps[frame[:-4]] = QPixmap(join(dir, frame))
        return pixmaps

    def setAnimations(self, pixmaps):
        raise NotImplementedError()

    def setAnim(self, anim):
        if anim == self.runningAnimName:
            return
        self.runningAnimName = anim
        self.runningAnim.stop()
        self.runningAnim = self.animations[anim]
        self.runningAnim.play()

    def setMission(self, mission):
        self.mission = mission
        self.mission()

    def setBorderless(self, center=True):
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.BypassGraphicsProxyWidget)
        self.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
        # Qt.NoDropShadowWindowHint
        # Qt.BypassWindowManagerHint
        # Qt.X11BypassWindowManagerHint
        # Qt.CustomizeWindowHint

        # Center it
        if center:
            geo = QDesktopWidget().availableGeometry()
            self.screenSize = geo.size()
            self.screenCenter = geo.center()
            self.setGeometry(self.screenCenter.x() - round(self.size[0] / 2), self.screenCenter.y() - round(self.size[1] / 2), self.size[0], self.size[1])

    def moveTo(self, x, y):
        self.setGeometry(x, y, self.width(), self.height())

    def moveAmt(self, dx, dy):
        self.setGeometry(self.x() + dx, self.y() + dy, self.width(), self.height())

    def moveToward(self, x, y, method='walk'):
        theta = asin((self.y - y) / (self.x - x))
        debug(theta)
        self.setAnim(method + self.dirFromAngle(theta).capitalize())
        self.moveAmt(self.moveSpeed)

    def dirFromAngle(self, ang):
        todo('add diagonal directions to this')
        # ang = absrad(ang)
        if isBetween(ang, 0, np.deg2rad(45), True, True) or isBetween(ang, np.deg2rad(315), np.deg2rad(360)):
            return 'up'
        elif isBetween(ang, np.deg2rad(45), np.deg2rad(135), True, False):
            return 'right'
        elif isBetween(ang, np.deg2rad(135), np.deg2rad(225), True, False):
            return 'down'
        elif isBetween(ang, np.deg2rad(225), np.deg2rad(315), True, False):
            return 'left'
        else:
            assert(False)


    def chainAnimiations(self, *animations):
        # Recursively call setNextAnim from when the current animation is finished, starting at 0
        def setNextAnim(index):
            if len(animations) < index:
                return
            else:
                self.setAnim(animations[index])
                self.runningAnim.finished.connect(lambda: setNextAnim(index+1))

        setNextAnim(0)

    # Default Missions
    def idle(self):
        self.setAnim("idle")

    def followMouse(self):
        while dist(*self.mouseCoord(), self.x(), self.y()) > self.closeEnoughToMouse:
            self.moveToward(mouseCoord())
        self.idle()

    def followMouseClicks(self):
        while dist(*self.lastClickPos, self.x(), self.y()) > self.closeEnoughToMouse:
            self.moveToward(lastClickPos)
        self.idle()

    def wander(self):
        # return (random.randint(0, self.screenSize.width()), random.randint(0, self.screenSize.height()))
        raise NotImplementedError()

    def wanderEdge(self):
        raise NotImplementedError()

    def wanderEdgeVauge(self):
        raise NotImplementedError()

    def wanderWindow(self):
        raise NotImplementedError()
