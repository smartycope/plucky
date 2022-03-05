import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QCursor, QPixmap, QBitmap
import PyQt5
from Plucky import Plucky
from Neko import Neko

if __name__ == "__main__":
    app = QApplication([])
    # window = Plucky()
    window = Neko()
    window.start()
    # window.started()
    sys.exit(app.exec_())
