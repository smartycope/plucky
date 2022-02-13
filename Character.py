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

from os.path import join, dirname

DIR = dirname(__file__)


class AlwaysInFrontCharacter(QLabel):
    def __init__(self):

        self.size = (35, 35)
        QLabel.__init__(self)
        self.setBorderless()


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
