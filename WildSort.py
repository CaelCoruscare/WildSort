import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


from ImageSorting.imageLogic import ImageLogic



app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)
engine.load('QtFiles/WildSort.qml')

sys.exit(app.exec())