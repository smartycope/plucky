import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QCursor, QPixmap, QBitmap
import PyQt5
from Plucky import Plucky
if __name__ == "__main__":
    app = QApplication([])
    window = Plucky()
    window.show()
    # app.setOverrideCursor(PyQt5.QtCore.Qt.BlankCursor)
    sys.exit(app.exec_())