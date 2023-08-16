import threading
import time
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

    smallDelay = 0.2

    #photoIndex is used to store notes in specific arrays here.
    notes = {-1:"You can write notes here when an image is open."}

    #This just handles initialization
    def __init__(self, dataMan: DataManager, eBridge: EmitterBridge):
        QObject.__init__(self)
        self.dataManager = dataMan
        self.emitterBridge = eBridge


    def isCategoryFinished(self):
        """Returns true if on the blank screen between categories or the blank screen at the end with the [Print Report] button"""
        return self.photoIndex == len(self.dataManager.photoURLs) -1

    def handleForwardEdgeCases(self, userResponse):
        #Handle case: First picture is being shown
        if self.categoryIndex == -1 and self.photoIndex == -1:
            #Hide the tutorial & show Next Category for AnyTrigger
            self.show_NextCategoryWillBe_InUI()
            self.photoIndex = -2
            return True
        
        #Handle case: The first "Next Category Will Be" screen is being shown
        if self.categoryIndex == -1 and self.photoIndex == -2:
            self.categoryIndex = 0
            self.setCategory_InUI()
            self.hide_NextCategoryWillBe_UI()

            #Doing this instead of calling setPhoto() because 
            #   forward() contains the logic for skipping over unnecessary photos
            self.photoIndex = -1
            self.forward(-2)
            return True
        
        #Handle case: all categories have been sorted.
        elif self.isCategoryFinished() and self.categoryIndex == len(self.dataManager.dataList):
            self.recordData(userResponse)
            self.emitterBridge.hidePhoto.emit()
            self.emitterBridge.showNextCategoryExplanation.emit("Report is now built to a spreadsheet (Need to implement)")
            return True
        
        #Handle case: Finished sorting a category
        elif self.isCategoryFinished():
            self.recordData(userResponse)
            self.flashIcon(userResponse)
            #Show the Next Category on a blank screen
            #self.doAfterSlightDelay(self.setPhotoIn_UI)
            self.setPhoto_InUI()
            self.photoIndex += 1
            return True
        
        #Handle Case: On a "Next Category" screen
        elif self.photoIndex == len(self.dataManager.photoURLs):
            self.emitterBridge.hideNextCategoryExplanation.emit()
            self.categoryForward()
            return True

        return False
        



########## Forward & Back logic

    def forward(self, userResponse):
        """Records data, increments the photo index until a non-skip photo is at the index, displays photo after delay"""
        if self.handleForwardEdgeCases(userResponse):
            return

        if userResponse != -2:
            self.recordData(userResponse)

        self.photoIndex +=1

        if self.dataManager.checkForSkip(self.photoIndex, self.categoryIndex):
            self.forward(-1)
            return

        else:
            #threading.Timer(0, self.flashIcon, [userResponse]).start()
            self.flashIcon(userResponse)
            time.sleep(self.smallDelay)
            self.setPhoto_InUI()
            

    def back(self):
        self.photoIndex -= 1
        if self.photoIndex == -1:
            self.categoryBack()
        else:
            self.emitterBridge.flashIcon.emit('back')
            time.sleep(self.smallDelay)
            self.setPhoto_InUI()

    def categoryForward(self):
        """Handles moving the category forward, then calls Forward again"""
        self.categoryIndex += 1
        self.setCategory_InUI()
        self.dataManager.copyParentData(self.categoryIndex) 

        #Doing this instead of calling setPhoto() because 
        #   forward() contains the logic for skipping over unnecessary photos
        self.photoIndex = -1
        self.forward(-2)

    def categoryBack(self):
        if self.categoryIndex > 0:
            self.categoryIndex -= 1
            self.photoIndex = len(self.dataManager.photoURLs)
            self.emitterBridge.flashIcon.emit('back')
            self.show_NextCategoryWillBe_InUI()

#########Supporting Functions

   
    def flashIcon(self, userAnswer):
        match userAnswer:
            case 1:
                self.emitterBridge.flashIcon.emit('yes')
            case 0:
                self.emitterBridge.flashIcon.emit('no')
            case _:
                pass
                

    def setPhoto_InUI(self):
        photo = self.dataManager.photoURLs[self.photoIndex]
        self.emitterBridge.updatePhoto.emit(photo)

    def setPhotoCounter_InUI(self):
        photoCounter = str(self.photoIndex) + '/' + str(self.dataManager.countPicsInCategory(self.categoryIndex))
        self.emitterBridge.updatePhotoCounter.emit(photoCounter)


    def setCategory_InUI(self):
        #TODO: Add a delay of 0.2 seconds
        self.emitterBridge.updateCategory.emit(self.dataManager.dataList[self.categoryIndex]['title'])
        
    def clearPhotoIn_UI(self):
        self.emitterBridge.updatePhoto.emit('')
        self.emitterBridge.updatePhotoCounter.emit('-/-')

    def show_NextCategoryWillBe_InUI(self):
        #TODO: Add a delay of 0.2 seconds
        self.emitterBridge.showNextCategoryExplanation.emit("Next Category will be: " + self.dataManager.dataList[self.categoryIndex + 1]['title'])
        self.emitterBridge.updatePhoto.emit('AppImages/restart-arrow.png')
        self.emitterBridge.updatePhotoCounter.emit('-/' + str(self.dataManager.countPicsInCategory(self.categoryIndex + 1)))

    def hide_NextCategoryWillBe_UI(self):
        self.emitterBridge.hideNextCategoryExplanation.emit()

    def show_AreYouReadyToPrintReportButton_InUI(self):
        #TODO: Add a delay of 0.2 seconds
        #TODO IMPLEMENT button and showing button.
        self.emitterBridge.updatePhoto.emit('')
        self.emitterBridge.updatePhotoCounter.emit('')
    
    def recordData(self, dataValue):
        """Sets data based on the photoIndex"""
        if self.photoIndex < len(self.dataManager.photoURLs) and self.photoIndex > -1: #Skip if we are on a blank screen between categories
            self.dataManager.dataList[self.categoryIndex]['data'][self.photoIndex] = dataValue
    