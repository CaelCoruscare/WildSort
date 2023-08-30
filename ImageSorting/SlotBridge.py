import threading
from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

import DataHandling.DataManager as data


import ImageSorting.ISortLogic as logic

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "com.isort.slotbridge"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SlotBridge(QObject):

    mutex = threading.Lock()

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
        if not self.mutex.acquire(blocking=False):
            return #Thread should end itself if the mutex is not available.
        #Need to make sure handling the choice is moved to ISortLogic

        #Make sure the list of pictures has been initialized.
        if not data.photoURLs:
            raise ValueError("pictureURLs List has not been initialized.", data.photoURLs)
        
        match choice.lower():
            case "yes":
                ###
                threading.Timer(0, logic.tryForward, [1]).start()
                #logic.tryForward(1)
                
            case "no":
                ###
                threading.Timer(0, logic.tryForward, [0]).start()
                #logic.tryForward(0)

            case "continue":
                ###
                threading.Timer(0, logic.tryForward, ['continue']).start()
                #logic.tryForward('continue')

            case "back":
                ###
                threading.Timer(0, logic.tryBack).start()
                #logic.tryBack()

            case _:
                raise ValueError("user choice passed in is not valid. Should be \'yes\',\'no\', or \'back\' (case insensitive)" , choice)

        #TODO:
        #Release Resource
        self.mutex.release()
    
    @Slot()
    def printReport(self):    
        logic.writeReport()

    @Slot(str, str)
    def setCameraAndLocation(self, camera, location):
        logic.setCameraAndLocation(camera, location)

    @Slot()
    def showTutorial(self):
        logic.showTutorial()

    @Slot(str)
    def setNote(self, note):
        print(note)
        logic.setNote(note)

    @Slot(result=str)
    def getNote(self):
        return logic.getNote()