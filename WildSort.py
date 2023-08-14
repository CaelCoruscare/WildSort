import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from ImageSorting.EmitterBridge import EmitterBridge


#from ImageSorting.ISortLogic import ISortLogic 
from ImageSorting.SlotBridge import SlotBridge



app = QGuiApplication(sys.argv)



engine = QQmlApplicationEngine()

emitterBridge = EmitterBridge()
engine.rootContext().setContextProperty("emitterBridge", emitterBridge)
slotBridge = SlotBridge(emitterBridge)
engine.rootContext().setContextProperty("slotBridge", slotBridge)

engine.quit.connect(app.quit)
engine.load('QtFiles/WildSort.qml')



sys.exit(app.exec())