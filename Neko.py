# This Python file uses the following encoding: utf-8
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
import pyautogui as ag
from globals import *
from Character import AlwaysInFrontCharacter
from os.path import join, dirname

DIR = dirname(__file__)

class Neko(AlwaysInFrontCharacter):
    framesDirectory=join(DIR, 'nekoFrames')
    def __init__(self):
        super().__init__(size=(35, 35),
                         frameSpeed=400, # In milliseconds
                         moveSpeed=20,   # In pixels - sorta
                         mission=self.followMouseClicks)

        self.minYawnTimeSec = 20
        self.maxYawnTimeSec = 360
        # self.yawnTimer = QTimer()
        self.sleepTimer = QTimer()
        # Seconds before Neko falls asleep after doing nothing
        self.tiredness = 10
        # self.movedRecently = False

    def setAnimations(self):
        pixmaps = self.loadPixmaps(self.framesDirectory)
        anims = {
            'sit':           Animation(self, -1, self.frameSpeed,       [pixmaps['sit']]),
            'up':            Animation(self, -1, self.frameSpeed,       [pixmaps['up1'],        pixmaps['up2']]),
            'down':          Animation(self, -1, self.frameSpeed,       [pixmaps['down1'],      pixmaps['down2']]),
            'left':          Animation(self, -1, self.frameSpeed,       [pixmaps['left1'],      pixmaps['left2']]),
            'right':         Animation(self, -1, self.frameSpeed,       [pixmaps['right1'],     pixmaps['right2']]),
            'upleft':        Animation(self, -1, self.frameSpeed,       [pixmaps['upLeft1'],    pixmaps['upLeft2']]),
            'upright':       Animation(self, -1, self.frameSpeed,       [pixmaps['upRight1'],   pixmaps['upRight2']]),
            'downleft':      Animation(self, -1, self.frameSpeed,       [pixmaps['downLeft1'],  pixmaps['downLeft2']]),
            'downright':     Animation(self, -1, self.frameSpeed,       [pixmaps['downRight1'], pixmaps['downRight2']]),
            'pawup':         Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawUp1'],     pixmaps['pawUp2']]),
            'pawdown':       Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawDown1'],   pixmaps['pawDown2']]),
            'pawleft':       Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawLeft1'],   pixmaps['pawLeft2']]),
            'pawright':      Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawRight1'],  pixmaps['pawRight2']]),
            'pawcenter':     Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawCenter'],  pixmaps['sit']]),
            'yawn':          Animation(self,  4, self.frameSpeed,       [pixmaps['yawn'],       pixmaps['sit']]),
            'sleep':         Animation(self, -1, self.frameSpeed * 2,   [pixmaps['sleep1'],     pixmaps['sleep2']]),
            'scratch':       Animation(self,  2, self.frameSpeed / 1.5, [pixmaps['scratch1'],   pixmaps['scratch2']]),
            'wakeUp':        Animation(self,  1, self.frameSpeed,       [pixmaps['awake']]),
            'fallAsleep':    Animation(self,  1, self.frameSpeed,       [pixmaps['sit'],        pixmaps['scratch1'], pixmaps['scratch2'], pixmaps['scratch1'], pixmaps['scratch2'], pixmaps['yawn']]),
            'sprayed':       Animation(self,  3, self.frameSpeed,       [pixmaps['awake']]),
            'eat':           Animation(self,  3, self.frameSpeed / 2,   [pixmaps['yawn'],       pixmaps['sit']]),
        }
        anims['idle'] = anims['sit']
        anims['die']  = anims['wakeUp']
        return anims

    def chase(self, dest=None):
        if dest is None:
            assert(self.runningAnimName == 'sleep')
            self.setAnim('wakeUp')
            self.runningAnim.finished.connect(self.chase, self.genNextDest())

        assert(dest)

        opp = self.y() - dest[1]
        adj = self.x() - dest[0]
        angle = math.atan2(adj, opp)  #Cope.normalize2rad(abs(math.atan2(self.y() - self.to[1], self.x() - self.to[0])))

        #  self.move(-math.sin(self.angle) / self.moveSpeed, -math.cos(self.angle) / self.moveSpeed)
        dx, dy = (math.cos(angle) * self.moveSpeed, math.sin(angle) * self.moveSpeed)


        _dir = self.dirFromAngle(angle)
        if _dir == Dir.UP:
            self.setAnim('walkUp')
        elif _dir == Dir.DOWN:
            self.setAnim('walkDown')
        elif _dir == Dir.LEFT:
            self.setAnim('walkLeft')
        elif _dir == Dir.RIGHT:
            self.setAnim('walkRight')

        def checkDest(tolerance):
            if self.mission is Mission.FOLLOW_MOUSE:
                dest = ag.position()
                if getDist(self.x(), self.y(), dest[0], dest[1]) < tolerance:
                    self.setAnim('pawCenter')
                    self.runningAnim.finished.connect(self.fallAsleep, -1)
            elif getDist(self.x(), self.y(), dest[0], dest[1]) < tolerance:
                self.fallAsleep(randint(self.minSleepCycles, self.maxSleepCycles))

        self.runningAnim.increment.connect(self.move) #, dx, dy)
        self.runningAnim.increment.connect(checkDest) #, self.closeEnoughTolerance)
        self.dx = round(dx)
        self.dy = round(dy)

    def fallAsleep(self, sleepAmount=None):
        if sleepAmount is None:
            sleepAmount = 10

        self.setAnim('fallAsleep')
        self.runningAnim.finished.connect(self.setAnim)

        def checkForMovement():
            if ag.position() != self.prevMouseLoc:
                self.chase()

        def setSleepTime(time):
            assert(self.runningAnim.name == 'sleep')
            if time < 0:
                assert(self.mission in (Mission.FOLLOW_MOUSE, Mission.FOLLOW_MOUSE_CLICKS))
                self.runningAnim.increment.connect(checkForMovement)

            self.runningAnim.laps = time
            self.runningAnim.finished.connect(self.chase)

        self.runningAnim.finished.connect(setSleepTime)

    def paw(self, _dir):
        self.setAnim('paw' + _dir.capitalize())

    def onMouseMoved(self, x, y):
        self.sleepTimer.stop()
        # self.movedRecently = True

    def followMouse(self):
        self.dynamicGoto(self.mouseCoord, self.closeEnoughToMouse, self.idle)

    @debug
    def idle(self):
        # self.chainAnimiations('fallAsleep', 'sleep')
        # self.chain2Animiations('fallAsleep', 'sleep')
        # if self.movedRecently:
            # self.setAnim('fallAsleep')
            # self.movedRecently = False
        # else:
        self.setAnim('sleep')

        # self.sleepTimer = QTimer()
        # self.sleepTimer.timeout.connect(self.fallAsleep)
        # self.sleepTimer.start(self.tiredness)
        # self.yawnTimer.timeout.connect(lambda: self.setAnim('yawn'))
        # self.yawnTimer.start(randint(self.minYawnTime * 1000, self.maxYawnTime * 1000))
