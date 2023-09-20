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
        #This needs to thread and return, so that the UI can continue updating. 
        # Otherwise the picture will freeze between rapid clicks
        thread = threading.Thread(target=self._handleChoice,args=[choice])
        thread.start()

    def _handleChoice(self, choice):
        #Mutex needs to be used or there will be data issues.
        if not self.mutex.acquire(blocking=False):
            return #Thread should end itself if the mutex is not available.

        #Make sure the list of pictures has been initialized.
        if not data.photoURLs:
            raise ValueError("pictureURLs List has not been initialized.", data.photoURLs)
        
        match choice.lower():
            case "yes":
                ###
                #threading.Timer(0, logic.tryForward, [1]).start()
                logic.tryForward(1)
                
            case "no":
                ###
                #threading.Timer(0, logic.tryForward, [0]).start()
                logic.tryForward(0)

            case "continue":
                ###
                #threading.Timer(0, logic.tryForward, ['continue']).start()
                logic.tryForward('continue')

            case "back":
                ###
                #threading.Timer(0, logic.tryBack).start()
                logic.tryBack()

            case _:
                raise ValueError("user choice passed in is not valid. Should be \'yes\',\'no\', or \'back\' (case insensitive)" , choice)

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
    
    @Slot(int, result=list)
    def flipValueInCategory(self, categoryIndex):
        print(f'Flip photo: {data.photoURLs[data.index.photo]} value for category: {data.dataList[categoryIndex].title}')
        #data.flipValueInCategory(categoryIndex)
        data.FlipValue(data.getCategory(categoryIndex))

        photoData = data.getPhotoData()
        return self._cleanPhotoData(photoData)

    @Slot(result=list)
    def getDataForPhoto(self):
        photoData = data.getPhotoData()
        return self._cleanPhotoData(photoData)
    
    def _cleanPhotoData(self, photoData):

        photoData = ['None' if (dat == None) else dat for dat in photoData]
        #photoData = [0 if (dat == 'skip') else dat for dat in photoData]

        return photoData