#!/usr/bin/env python
import os
from pathlib import Path
import sys

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

import PySide6.QtCore as QtCore

from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


#from ImageSorting.ISortLogic import ISortLogic 
from ImageSorting.SlotBridge import SlotBridge

import ImageSorting.CallsToUI as callsToUI


# https://stackoverflow.com/a/42615559/6622587
application_path = (
    sys._MEIPASS
    if getattr(sys, "frozen", False)
    else os.path.dirname(os.path.abspath(__file__))
)

if __name__ == "__main__":
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


    file = os.path.join(application_path, "QtFiles/WildSort.qml")
    engine.load(QtCore.QUrl.fromLocalFile(file))

    #engine.load('HelloApp.qml')


    
    sys.exit(app.exec())


    # qml_file = Path(__file__).parent / 'QtFiles/WildSort.qml'
    # engine.load(qml_file)