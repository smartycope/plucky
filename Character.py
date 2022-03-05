# This Python file uses the following encoding: utf-8
from pynput import mouse
import sys, os, time, random, math
from PyQt5.QtWidgets import QApplication, QMainWindow
from Animation import Animation
from PyQt5 import *
# from PyQt5 import QtCore, QtGui, QtMultimedia, QtWidgets, uic
from PyQt5.QtCore import *
from PyQt5.QtCore import QEvent, Qt, QTimer, QSize, QThread
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
# from PyQt5.QtWidgets import QApplication, QFileDialog, QMainWindow, QWidget
import numpy as np
from copy import deepcopy
from time import sleep

from Cope import *
# import pyautogui as ag
from pyautogui import position as mouseCoord
from globals import *
import asyncio
from math import asin, sin, cos, atan2, radians, degrees

from os.path import join, dirname

DIR = dirname(__file__)

import signal

class AlwaysInFrontCharacter(QLabel):
    closeEnoughToMouse = 50
    # UPDATE_INTERVAL = 250 # In milliseconds
    UPDATE_INTERVAL = 1000 # In milliseconds

    def __init__(self, size,
                       frameSpeed=400, # In milliseconds
                       moveSpeed=20,   # In pixels - sorta
                       minSleepCycles=5,
                       maxSleepCycles=100,
                       mission=None,
                       **kwargs):
        self.size = size
        QLabel.__init__(self, **kwargs)
        self.setBorderless()

        self.mouseListener = mouse.Listener(on_click=self._onMouseClicked, on_move=self.onMouseMoved, on_scroll=self.onMouseScrolled)
        if mission == self.followMouseClicks:
            self.mouseListener.start()

        self.frameSpeed = frameSpeed
        self.moveSpeed = moveSpeed

        self.mission = self.idle if mission is None else mission

        self.animations = ZerosDict(self.setAnimations())

        if self.animations['idle'] is None:
            raise UserWarning('Animations must include an idle animation!')

        self.lastClickPos = self.mouseCoord()

        self.runningAnimName = 'idle'
        self.runningAnim = self.animations['idle']
        self.show()

        # Basically just start a new thread
        # QTimer.singleShot(10, Qt.CoarseTimer, self.mission)

        # self.timer = QTimer()
        # self.timer.timeout.connect(self.mission)
        # self.timer.setInterval(self.UPDATE_INTERVAL)
        # self.timer.setInterval(10)
        # self.timer.start()

        # self.finished.connect(QObject.deleteLater)
        # workerThread.start()

        self.thread = QThread()
        self.moveToThread(self.thread)
        self.thread.started.connect(self.mission)
        self.thread.finished.connect(self.die)
        self.thread.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        signal.signal(signal.SIGINT, self.die)

        # self.mission()
        # asyncio.run(self.mission)

    def start(self):
        self.thread.start()

    def _onMouseClicked(self, x, y, button, pressed):
        if pressed:
            self.lastClickPos = (x, y)

        # debug(f"button {button} pressed")

        # debug(self.rect())
        # debug((x, y))
        if pressed and button == mouse.Button.middle and QRect(self.x(), self.y(), self.width(), self.height()).contains(x, y):
            # debug()
            # self.close.emit()
            # self.destroyed.emit()
            self.close()
            # self.die()
            # self.closeEvent.emit()

        self.onMouseClicked(x, y, button, pressed)


    def onMouseClicked(self, x, y, button, pressed):
        pass

    def onMouseMoved(self, x, y):
        pass

    def onMouseScrolled(self, x, y, dx, dy):
        pass

    def mouseCoord(self):
        c = mouseCoord()
        return (c.x - (self.size[0] / 2), c.y - (self.size[1] / 2))

    @staticmethod
    def loadPixmaps(dir, size=None):
        """ Load all the frames """
        pixmaps = {}
        for frame in os.listdir(dir):
            pixmaps[frame[:-4]] = QPixmap(join(dir, frame))
            if size is not None:
                pixmaps[frame[:-4]] = pixmaps[frame[:-4]].scaled(QSize(*size))
        return pixmaps

    def setAnimations(self):
        raise NotImplementedError()

    def setAnim(self, anim):
        # debug(f'running animation {anim}')
        if anim == self.runningAnimName:
            return
        self.runningAnimName = anim
        self.runningAnim.stop()
        if self.animations[anim] is None:
            raise UserWarning(f"{type(self).__name__} does not have a {anim} animation specified")
        self.runningAnim = self.animations[anim]
        self.runningAnim.play()

    def setMission(self, mission):
        self.mission = mission
        self.mission()

    def setBorderless(self, center=True):
        self.setAttribute( Qt.WA_TranslucentBackground)
        self.setAttribute( Qt.WA_NoSystemBackground)
        self.setAttribute( Qt.WA_X11DoNotAcceptFocus)
        self.setAttribute( Qt.WA_DeleteOnClose)
        self.setAttribute( Qt.WA_TransparentForMouseEvents)
        self.setWindowFlag(Qt.WindowTransparentForInput)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowFlag(Qt.BypassGraphicsProxyWidget)
        self.setWindowFlag(Qt.WindowDoesNotAcceptFocus)
        # Qt.WA_OpaquePaintEvent
        # Qt.NoDropShadowWindowHint
        # Qt.BypassWindowManagerHint
        # Qt.X11BypassWindowManagerHint
        # Qt.CustomizeWindowHint
        # Qt.WA_PaintOnScreen
        # Qt.WA_SetCursor
        # Qt.WA_LayoutOnEntireRect
        # Qt.WA_LayoutUsesWidgetRect
        # Qt.WA_NoChildEventsForParent
        # Qt.WA_NoChildEventsFromChildren

        # Center it
        if center:
            geo = QDesktopWidget().availableGeometry()
            self.screenSize = geo.size()
            self.screenCenter = geo.center()
            self.setGeometry(self.screenCenter.x() - round(self.size[0] / 2), self.screenCenter.y() - round(self.size[1] / 2), self.size[0], self.size[1])

    def getLastClickPos(self):
        return self.lastClickPos

    def moveTo(self, x, y):
        self.setGeometry(x, y, self.width(), self.height())

    def moveAmt(self, dx, dy):
        self.setGeometry(round(self.x() + dx), round(self.y() + dy), self.width(), self.height())

    def goto(self, x, y, tolerance):
        # step = self.stepToward(x, y)
        if dist(x, y, self.x(), self.y()) > tolerance:
            # step.send(None)
            self.stepToward(x, y)
        else:
            return

    def dynamicGoto(self, getCoordFunc, tolerance, idleFunc):
        x, y = getCoordFunc()
        if dist(x, y, self.x(), self.y()) > tolerance:
            self.stepToward(x, y)
        else:
            idleFunc()

    def stepToward(self, x, y):
        theta = atan2(y-self.y(), x-self.x())
        self.setAnim(self.dirFromAngle(theta))
        self.moveAmt(self.moveSpeed * cos(theta), self.moveSpeed * sin(theta))
        # self.runningAnim.incremented.connect(self.mission)
        self.runningAnim.increment()
        # return

    def dirFromAngle(self, ang, deg=False):
        if not deg:
            ang = degrees(ang)
        if ang < 0:
            ang = 360 + ang

        if self.animations['upright']:
            if isBetween(ang, 0, 22.5, True, True) or isBetween(ang, 337.5, 360):
                return 'right'
            elif isBetween(ang, 22.5, 67.5, True, False):
                return 'downright'
            elif isBetween(ang, 67.5, 112.5, True, False):
                return 'down'
            elif isBetween(ang, 112.5, 157.5, True, False):
                return 'downleft'
            elif isBetween(ang, 157.5, 202.5, True, False):
                return 'left'
            elif isBetween(ang, 202.5, 247.5, True, False):
                return 'upleft'#
            elif isBetween(ang, 247.5, 292.5, True, False):
                return 'up'
            elif isBetween(ang, 292.5, 337.5, True, False):
                return 'upright'#
            else:
                debug(ang, color=Colors.ALERT)
                return 'idle'
        else:
            if isBetween(ang, 0, 45, True, True) or isBetween(ang, 315, 360):
                return 'right'
            elif isBetween(ang, 45, 135, True, False):
                return 'down'
            elif isBetween(ang, 135, 225, True, False):
                return 'left'
            elif isBetween(ang, 225, 315, True, False):
                return 'up'
            else:
                debug(ang, color=Colors.ALERT)
                return 'idle'

    def chain2Animiations(self, a, b):
        self.setAnim(a)
        self.runningAnim.finished.connect(lambda: self.setAnim(b))
        # self.runningAnim.finished.connect(lambda x=None: print(x, ': thing'))
        # self.runningAnim.finished.connect(FunctionCall(self.setAnim, b))

    def chainAnimiations(self, *animations):
        # self.setAnim()
        pass
        # Recursively call setNextAnim from when the current animation is finished, starting at 0
        """
        def setNextAnim(index):
            if len(animations) < index:
                return
            else:
                self.setAnim(animations[index])
                self.runningAnim.finished.connect(lambda: setNextAnim(index+1))

        setNextAnim(0)
        """

    def closeEvent(self, event):
        # event.accept()
        # debug()
        self.die()
        return

    # Default Missions
    def idle(self):
        self.setAnim("idle")

    def followMouse(self):
        self.dynamicGoto(self.mouseCoord, self.closeEnoughToMouse, self.idle)

    def followMouseClicks(self):
        self.dynamicGoto(self.getLastClickPos, self.closeEnoughToMouse, self.idle)

    def wander(self):
        # return (random.randint(0, self.screenSize.width()), random.randint(0, self.screenSize.height()))
        raise NotImplementedError()

    def wanderEdge(self):
        raise NotImplementedError()

    def wanderEdgeVauge(self):
        raise NotImplementedError()

    def wanderWindow(self):
        raise NotImplementedError()

    def die(self, *args):
        def end():
            # sleep(1)
            # self.timer.stop()
            self.destroy()
            exit(0)
        # debug()
        # self.timer.stop()
        self.setAnim('die')
        self.runningAnim.play()
        self.runningAnim.finished.connect(end)
        self.runningAnim.lapped.connect(end)
        # while True:
            # self.runningAnim.increment()
