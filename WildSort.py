import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from ImageSorting.EmitterBridge import EmitterBridge


#from ImageSorting.ISortLogic import ISortLogic 
from ImageSorting.SlotBridge import SlotBridge

import ImageSorting.CallsToUI as callsToUI

print("")
print("")
print("")
print("Starting...")

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()

emitterBridge = callsToUI.emitter
engine.rootContext().setContextProperty("emitterBridge", emitterBridge)
slotBridge = SlotBridge()
engine.rootContext().setContextProperty("slotBridge", slotBridge)

engine.quit.connect(app.quit)
engine.load('QtFiles/WildSort.qml')


 
sys.exit(app.exec())