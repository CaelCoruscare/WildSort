import os
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtCore import QObject, Signal, Property

from DataHandling.DataManager import DataManager
from DataHandling.ReportBuilder import reportBuilder


from ImageSorting.ISortLogic import ISortLogic

from ImageSorting.EmitterBridge import EmitterBridge

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "com.isort.slotbridge"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SlotBridge(QObject):

    def __init__(self, eBridge: EmitterBridge):
        QObject.__init__(self)
        self.emitterBridge = eBridge
        self.dataManager = DataManager()
        self.logic = ISortLogic(self.dataManager, self.emitterBridge)
        self.emitterBridge.wtf()

    #Accept a folder URL
    @Slot(str)
    def handleSetFolder(self, folderURL):
        #Fix for QT Filepath:  
        #   file:///Users/test/Pictures --> /Users/test/Pictures
        folderURLFixed = folderURL[7:]

        self.dataManager.folderChosen(folderURLFixed)


        #Set the UI to "Is there: Any Trigger?"
        self.emitterBridge.updateCategory.emit("Any Trigger")
        self.emitterBridge.updatePhotoCounter.emit('0' + "/" + str(len(self.dataManager.photoURLs)))
        
        #Make sure the pictures start from the beginning 
        #   (for once opening multiple folders is implemented)
        self.logic.picIndex = -1
        self.logic.categoryIndex = 0

        self.emitterBridge.updatePhotoCounter.emit("")
        self.emitterBridge.showExplanation.emit("Use the L key and ; key as Yes and No, to cycle through the images. If you need to go back, use the \' key")
     
    @Slot(str)
    def choiceMade(self, choice):
        #Make sure the list of pictures has been initialized.
        if not self.dataManager.photoURLs:
            raise ValueError("pictureURLs List has not been initialized.", self.dataManager.photoURLs)
        
        match choice.lower():
            case "yes":
                if not self.logic.isOnBlankScreen():
                    self.emitterBridge.flashIcon.emit("yes")
                ###
                self.logic.photoForward(1)
                
            case "no":
                if not self.logic.isOnBlankScreen():
                    self.emitterBridge.flashIcon.emit("no")
                ###
                self.logic.photoForward(0)

            case "back":
                ###
                self.logic.photoBack()

            case _:
                raise ValueError("user choice passed in is not valid. Should be \'yes\',\'no\', or \'back\' (case insensitive)" , choice)

    
    @Slot(str)
    def recordNote(self, note):
        print(note)
        self.notes[self.picIndex] = note

    @Slot(result=str)
    def getNote(self):
        return self.notes.get(self.picIndex, "")