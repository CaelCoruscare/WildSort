from PySide6.QtCore import QObject, Slot
from PySide6.QtQml import QmlElement

import DataHandling.DataManager as DataManager
from DataHandling.DataManager import index

import DataHandling.ReportBuilder as ReportBuilder


import ImageSorting.SortLogic as SortLogic
from WildElements import WildScreens as Screens

from ImageSorting.WildMutex import mutexify_ButAllowUIUpdates, wildMutex

import ImageSorting.CallsToUI as ui

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "com.isort.slotbridge"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class SlotBridge(QObject):

    def __init__(self):
        QObject.__init__(self)



######-------------
### UI Blocking Methods
######-------------

    #Accept a folder URL
    @Slot(str)
    def folderChosen(self, folderURL):
        mutexify_ButAllowUIUpdates(
            self._handleFolderChosen
            , [folderURL]
            )

    def _handleFolderChosen(self, folderURL):
        print(folderURL)

        if DataManager.tryInitializeFromFolder(folderURL):
            Screens.screenManager.next()
    
            DataManager.yoloPhotoURLs = DataManager.WildAI.yoloPhotos(DataManager.photoURLs)

            print(DataManager.yoloPhotoURLs)

            #This is for the Notes popup
            ui.createCategoryCheckboxes(
                categoryTitles=[category.title for category in DataManager.dataList], 
                indentation=[category.countAncestors() for category in DataManager.dataList])

            ReportBuilder.folderOfPhotos = DataManager.ImageExtractor._cleanURL(folderURL)

            Screens.screenManager.next()
        
    @Slot()
    def nextScreen(self):
        if not wildMutex.acquire(blocking=False):
            return
        
        Screens.screenManager.next()
        if type(Screens.screenManager.currentScreen) is Screens.ImageViewer:
            SortLogic.nextPhoto()

        wildMutex.release()

    @Slot()
    def previousScreen(self):
        mutexify_ButAllowUIUpdates(
            Screens.screenManager.back
            , []
            )
            


    @Slot()
    def previousPhoto(self):
        ui.flashIcon('back')

        mutexify_ButAllowUIUpdates(
            SortLogic.previousPhoto()
            , []
            )
        
    @Slot(str)
    def choiceMade(self, choice):
        ui.flashIcon(choice)

        mutexify_ButAllowUIUpdates(
            SortLogic.choiceMade
            , [choice]
            )
        return
    
    @Slot()
    def printReport(self):
        if not wildMutex.acquire(blocking=False):
            return 
        
        ReportBuilder.buildReports_Human(DataManager.dataList, DataManager.photoURLs, DataManager.notes)
        Screens.screenManager.next()

        wildMutex.release()

######-------------
### Blocks other Python Actions but allows UI to update
######-------------

    @Slot(str, str)
    def setCameraAndLocation(self, camera, location):
        ReportBuilder.camera = camera
        ReportBuilder.location = location

#####-----------
###NOTES Below
#####-----------

    @Slot(str)
    def setNote(self, note):
        DataManager.setNote(note)

    @Slot(result=str)
    def getNote(self):
        return DataManager.getNote()
    
    @Slot(int, result=list)
    def flipValueInCategory(self, categoryIndex):
        print(f'Flip photo: {DataManager.photoURLs[DataManager.index.photo]} value for category: {DataManager.dataList[categoryIndex].title}')
        #data.flipValueInCategory(categoryIndex)
        DataManager.FlipValue(DataManager.getCategory(categoryIndex), index.photo)

        photoData = DataManager.getPhotoData()
        return self._cleanPhotoData(photoData)

    @Slot(result=list)
    def getDataForPhoto(self):
        photoData = DataManager.getPhotoData()
        return self._cleanPhotoData(photoData)
    
    def _cleanPhotoData(self, photoData):

        photoData = ['None' if (dat == None) else dat for dat in photoData]
        #photoData = [0 if (dat == 'skip') else dat for dat in photoData]

        return photoData
