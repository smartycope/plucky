from PyQt5.QtCore import QTimer, pyqtSignal
from Cope import Signal, debug
from time import sleep

class Animation:
    def __init__(self, subject, laps, delay, frames):
        self.subject = subject
        self.frames = frames
        self.len = len(self.frames)
        self.curFrame = 0
        self.playing = False
        self.laps = laps
        self.lap = 0
        self.done = False
        self.finished = Signal()
        self.lapped = Signal()
        self.incremented = Signal()
        self.delay = delay

        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.setInterval(round(self.delay))

    def update(self, frames=1):
        self.curFrame += frames
        if self.curFrame >= self.len:
            self.lap += 1
            if self.lap >= self.laps and self.laps > 0:
                self.done = True
                self.stop()
                self.finished.emit()
                debug(f'finished animation')
                return
            else:
                self.lapped.emit()
                self.curFrame = 0

        self.subject.setPixmap(self.frames[self.curFrame])
        # self.subject.update()
        # self.subject.show()
        self.subject.repaint()
        self.incremented.emit()

    def play(self):
        self.timer.start()
        self.playing = True
        self.lap = 0
        self.curFrame = 0

    def pause(self):
        self.timer.stop()
        self.playing = False

    def stop(self):
        self.pause()
        self.playing = False

    def resume(self):
        self.timer.start()
        self.playing = True

    def increment(self, blocking=True, frames=1):
        """ To decrement, set frames to negative
            Incrementing multiple frames skips that many frames ahead, it doesn't play them all
        """
        if self.playing:
            self.pause()

        self.update(frames)
        if blocking:
            sleep(self.delay / 1000)

    def __add__(self, other):
        other.pause()
        self.finished.connect(other.play)
        return self
