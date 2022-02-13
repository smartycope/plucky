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

class Plucky(AlwaysInFrontCharacter):
    def __init__(self):
        super().__init__(size=(35, 35),
                         framesDirectory=join(DIR, 'pluckyFrames'),
                         frameSpeed=400, # In milliseconds
                         moveSpeed=20,   # In pixels - sorta
                        )

        self.minYawnTimeSec = 20
        self.maxYawnTimeSec = 360
        self.mission = self.followMouse

    def setAnimations(self, pixmaps):
        sit = Animation(self, -1, self.frameSpeed, [pixmaps['sit']]),
        return {
            'idle':          sit,
            'sit':           sit,
            'walkUp':        Animation(self, -1, self.frameSpeed,       [pixmaps['up1'],        pixmaps['up2']]),
            'walkDown':      Animation(self, -1, self.frameSpeed,       [pixmaps['down1'],      pixmaps['down2']]),
            'walkLeft':      Animation(self, -1, self.frameSpeed,       [pixmaps['left1'],      pixmaps['left2']]),
            'walkRight':     Animation(self, -1, self.frameSpeed,       [pixmaps['right1'],     pixmaps['right2']]),
            'walkUpLeft':    Animation(self, -1, self.frameSpeed,       [pixmaps['upLeft1'],    pixmaps['upLeft2']]),
            'walkUpRight':   Animation(self, -1, self.frameSpeed,       [pixmaps['upRight1'],   pixmaps['upRight2']]),
            'walkDownLeft':  Animation(self, -1, self.frameSpeed,       [pixmaps['downLeft1'],  pixmaps['downLeft2']]),
            'walkDownRight': Animation(self, -1, self.frameSpeed,       [pixmaps['downRight1'], pixmaps['downRight2']]),
            'pawUp':         Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawUp1'],     pixmaps['pawUp2']]),
            'pawDown':       Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawDown1'],   pixmaps['pawDown2']]),
            'pawLeft':       Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawLeft1'],   pixmaps['pawLeft2']]),
            'pawRight':      Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawRight1'],  pixmaps['pawRight2']]),
            'pawCenter':     Animation(self,  3, self.frameSpeed / 1.5, [pixmaps['pawCenter'],  pixmaps['sit']]),
            'yawn':          Animation(self,  4, self.frameSpeed,       [pixmaps['yawn'],       pixmaps['sit']]),
            'sleep':         Animation(self, -1, self.frameSpeed / 1.5, [pixmaps['sleep1'],     pixmaps['sleep2']]),
            'scratch':       Animation(self,  2, self.frameSpeed / 1.5, [pixmaps['scratch1'],   pixmaps['scratch2']]),
            'wakeUp':        Animation(self,  1, self.frameSpeed,       [pixmaps['awake']]),
            'fallAsleep':    Animation(self,  1, self.frameSpeed,       [pixmaps['sit'],        pixmaps['scratch1'], pixmaps['scratch2'], pixmaps['scratch1'], pixmaps['scratch2'], pixmaps['yawn']]),
            'sprayed':       Animation(self,  3, self.frameSpeed,       [pixmaps['awake']]),
            'eat':           Animation(self,  3, self.frameSpeed / 2,   [pixmaps['yawn'],       pixmaps['sit']]),
        }
