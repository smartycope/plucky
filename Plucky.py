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

SIZE = (30, 30)

class Plucky(AlwaysInFrontCharacter):
    framesDirectory=join(DIR, 'pluckyFrames')
    def __init__(self):
        super().__init__(size=SIZE,
                         frameSpeed=400, # In milliseconds
                         moveSpeed=20,   # In pixels - sorta
                         mission=self.followMouseClicks)

    def setAnimations(self):
        rtn = {}
        for anim in ('down', 'up', 'left', 'right', 'pecking', 'downSitting', 'upSitting', 'leftSitting', 'rightSitting'):
            rtn[anim] = Animation(self, -1, self.frameSpeed, list(self.loadPixmaps(join(self.framesDirectory, anim), SIZE).values()))


        rtn['downSitting'].delay /= 2
        rtn['idle'] = rtn['downSitting']
        rtn['die'] = rtn['pecking']

        return rtn