import os
import threading
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtCore import QObject, Signal, Property

import DataHandling.DataManager as dataManager
from DataHandling.ReportBuilder import reportBuilder


import ImageSorting.ISortLogic as logic

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "com.isort.slotbridge"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SlotBridge(QObject):

    def __init__(self):
        QObject.__init__(self)

    #Accept a folder URL
    @Slot(str)
    def folderChosen(self, folderURL):
        #Fix for QT Filepath:  
        #   file:///Users/test/Pictures --> /Users/test/Pictures
        folderURLFixed = folderURL[7:]

        logic.folderChosen(folderURLFixed)

        
    @Slot(str)
    def choiceMade(self, choice):
        #TODO: Need to add a shared resource here
        #Claim Resource

        #Need to make sure handling the choice is moved to ISortLogic

        #Make sure the list of pictures has been initialized.
        if not dataManager.photoURLs:
            raise ValueError("pictureURLs List has not been initialized.", dataManager.photoURLs)
        
        match choice.lower():
            case "yes":
                ###
                threading.Timer(0, logic.forward, [1]).start()
                #self.logic.forward(1)
                
            case "no":
                ###
                threading.Timer(0, logic.forward, [0]).start()
                #self.logic.forward(0)

            case "back":
                ###
                threading.Timer(0, logic.tryBack).start()
                #self.logic.back()

            case _:
                raise ValueError("user choice passed in is not valid. Should be \'yes\',\'no\', or \'back\' (case insensitive)" , choice)

        #TODO:
        #Release Resource
    
    @Slot(str)
    def setNote(self, note):
        print(note)
        logic.setNote(note)

    @Slot(result=str)
    def getNote(self):
        return logic.getNote()