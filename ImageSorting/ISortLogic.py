import threading
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtCore import QObject, Signal, Property


from DataHandling.DataManager import DataManager
from DataHandling.ReportBuilder import reportBuilder


from ImageSorting.EmitterBridge import EmitterBridge



class ISortLogic(QObject):

    photoIndex = -1
    categoryIndex = 0
    typeIndex = 0

    looking4Changed = Signal(str)
    pictureChanged = Signal(str)
    flashIcon = Signal(str)

    #photoIndex is used to store notes in specific arrays here.
    notes = {-1:"You can write notes here when an image is open."}

    #This just handles initialization
    def __init__(self, dataMan: DataManager, eBridge: EmitterBridge):
        QObject.__init__(self)
        self.dataManager = dataMan
        self.emitterBridge = eBridge

    


########## Forward & Back logic

    def photoForward(self, wasTriggerSeen):
        """increments the photo index and handles all resulting logic"""
        self.recordData(wasTriggerSeen)
        self.photoIndex +=1

        if self.isOnBlankScreen():
            self.show_NextCategoryWillBe()

        elif self.photoIndex > len(self.dataManager.photoURLs):
            self.categoryForward() 

        elif self.dataManager.checkForSkip(self.photoIndex, self.categoryIndex):
            self.photoForward(-1)
            pass

        else:
            threading.Timer(0.2, self.setPhoto).start()
            

    def photoBack(self):
        self.photoIndex -= 1
        if self.photoIndex == -1:
            self.categoryBack()
        else:
            self.setPhoto()

    def categoryForward(self):
        self.categoryIndex += 1
        if self.categoryIndex == len(self.dataManager.dataList):
            self.show_AreYouReadyToPrintReport_Button() #Last chance before writing report
        elif self.categoryIndex < len(self.dataManager.dataList):
            self.dataManager.copyParentData(self.categoryIndex) 
            self.photoIndex = -1
            self.setCategory()
            self.photoForward(-2)

    def categoryBack(self):
        if self.categoryIndex > 0:
            self.categoryIndex -=1
            self.photoIndex = len(self.dataManager.photoURLs)
            self.emitterBridge.flashIcon.emit('back')
            self.show_NextCategoryWillBe()

#########Supporting Functions

   
    def isOnBlankScreen(self):
        """Returns true if on the blank screen between categories or the blank screen at the end with the [Print Report] button"""
        return self.photoIndex == len(self.dataManager.photoURLs)

    def setPhoto(self):
        #TODO: Add a delay of 0.2 seconds
        self.emitterBridge.updatePhoto.emit(self.dataManager.photoURLs[self.photoIndex])
        
        self.emitterBridge.updatePhotoCounter.emit(str(self.photoIndex) + '/' + str(self.dataManager.countPicsInCategory(self.categoryIndex)))
    
    def setCategory(self):
        #TODO: Add a delay of 0.2 seconds
        self.emitterBridge.updateCategory.emit(self.dataManager.dataList[self.categoryIndex]['title'])
        
    def clearPhoto(self):
        self.emitterBridge.updatePhoto.emit('')
        self.emitterBridge.updatePhotoCounter.emit('-/-')

    def show_NextCategoryWillBe(self):
        #TODO: Add a delay of 0.2 seconds
        #TODO: Show Next Category (Need to add the next category textbox to QML)
        if self.categoryIndex == len(self.dataManager.dataList):
            pass
        self.emitterBridge.updatePhoto.emit('AppImages/restart-arrow.png')
        self.emitterBridge.updatePhotoCounter.emit('-/' + str(self.dataManager.countPicsInCategory(self.categoryIndex + 1)))
                                

    def show_AreYouReadyToPrintReport_Button(self):
        #TODO: Add a delay of 0.2 seconds
        #TODO IMPLEMENT button and showing button.
        self.emitterBridge.updatePhoto.emit('')
        self.emitterBridge.updatePhotoCounter.emit('')
    
    def recordData(self, dataValue):
        """Sets data based on the photoIndex"""
        if self.photoIndex < len(self.dataManager.photoURLs) and self.photoIndex != -1: #Skip if we are on a blank screen between categories
            self.dataManager.dataList[self.categoryIndex]['data'][self.photoIndex] = dataValue
    