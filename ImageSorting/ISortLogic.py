from dataclasses import dataclass
from enum import Enum
import time
from types import SimpleNamespace

from DataHandling import DataManager as dataManager
import ImageSorting.CallsToUI as ui


#index = SimpleNamespace(photo = -1, category = 0)

index = dataManager.Index(-1,0)


smallDelay = 0.2

#index.photo is used to store notes in specific arrays here.
notes = {-1:"You can write notes here when an image is open."}

class EdgeCase(Enum):
    SHOWINGTUTORIAL = 1
    FIRSTSHOWINGNEXTCATEGORY = 2
    SHOWINGNEXTCATEGORY = 3
    ENDOFCATEGORY = 4
    NONE = 5

edgeCase = EdgeCase.SHOWINGTUTORIAL


def handleForwardEdgeCases(userResponse):
    global edgeCase

    if edgeCase == EdgeCase.SHOWINGTUTORIAL:
        ui.show_Explanation(None)#Hide the tutorial
        ui.show_NextCategoryWillBe('Any Trigger')
        ui.setPhotoCounter('-/' + str(dataManager.countPhotosInCategory(index.category)))

        edgeCase = EdgeCase.FIRSTSHOWINGNEXTCATEGORY

        return True
    
    elif edgeCase == EdgeCase.FIRSTSHOWINGNEXTCATEGORY:
        ui.hide_NextCategoryWillBe()
        ui.setCategory('Any Trigger')
        ui.setPhotoCounter('1/' +  str(dataManager.countPhotosInCategory(index.category)))
        ui.setPhoto(dataManager.getPhoto(0))
        edgeCase = EdgeCase.NONE

        return True
    
    elif edgeCase == EdgeCase.ENDOFCATEGORY:
        recordData(userResponse)
        ui.flashIcon(userResponse) 

        if index.category == len(dataManager.dataList): #If end of categories
            ui.show_AreYouReadyToPrintReport()
        else: 
            ui.show_NextCategoryWillBe(dataManager.getCategoryTitle(index.category + 1))
            dataManager.findSkipsFromParentData(index.category + 1) # Need to do this so the next line functions
            ui.setPhotoCounter('-/' + str(dataManager.countPhotosInCategory(index.category + 1)))
            edgeCase = EdgeCase.SHOWINGNEXTCATEGORY
            
        ui.setPhoto(None)
        ui.setCategory(None)

        index.photo += 1
        return True
    
    elif edgeCase == EdgeCase.SHOWINGNEXTCATEGORY:
        ui.show_NextCategoryWillBe(None)

        edgeCase = EdgeCase.NONE

        categoryForward()
        
        return True
    
    
    
    

    return False
    



########## Forward & Back logic
def forward(userResponse):
    """Records data, increments the photo index until a non-skip photo is at the index, displays photo after delay"""
    if handleForwardEdgeCases(userResponse):
        return

    #"-2" allows forward() to be called without setting data or flashing an icon.
    if userResponse != -2:
        recordData(userResponse)
        ui.flashIcon(userResponse)

    index.photo +=1

    if index.photo == len(dataManager.photoURLs) - 1:
        global edgeCase
        edgeCase = EdgeCase.ENDOFCATEGORY

    if dataManager.checkForSkip(index):
        forward(-2)
    else:
        time.sleep(smallDelay)
        ui.setPhoto(dataManager.getPhoto(index.photo))
        ui.setPhotoCounter(
            str(dataManager.countPicsAsked(index)) + 
            '/' + 
            str(dataManager.countPhotosInCategory(index.category))
            )


def back():
    # if handleBackEdgeCases()
    # return

    # Index.photo -= 1

    # if index.photo == 0:
    # backCategory()

    # elif dM.checkSkip(index.photo):
    # back()

    # Else:
    # flashIcon()
    # showphoto()


    index.photo -= 1
    if index.photo == -1:
        categoryBack()
    else:
        ui.flashIcon('back')
        time.sleep(smallDelay)
        ui.setPhoto(dataManager.photoURLs[index.photo])
        ui.setPhotoCounter(str(dataManager.countPicsAsked(index)) + '/' + str(dataManager.countPhotosInCategory(index.category)))

def categoryForward():
    """Handles moving the category forward, then calls Forward again"""
    index.category += 1
    ui.setCategory(dataManager.getCategoryTitle(index.category))
    dataManager.findSkipsFromParentData(index.category) 

    #Doing this instead of calling setPhoto() because 
    #   forward() contains the logic for skipping over unnecessary photos
    index.photo = -1
    forward(-2)

def categoryBack():
    if index.category > 0:
        index.category -= 1
        index.photo = len(dataManager.photoURLs)
        ui.flashIcon('back')
        ui.show_NextCategoryWillBe(
            dataManager.dataList[index.category + 1]['title'], 
            str(dataManager.countPicsInCategory(index.category + 1))
            )
########

#########Supporting Functions




def recordData(dataValue):
    """Sets data based on the index.photo"""
    if index.photo < len(dataManager.photoURLs) and index.photo > -1: #Skip if we are on a blank screen between categories
        dataManager.dataList[index.category]['data'][index.photo] = dataValue

def folderChosen(folderURL):
    #Datamanager handles the data
    dataManager.folderChosen(folderURL)

    ui.show_Explanation(
        "Use the [L] key and [;] key as Yes and No, to cycle through the images. If you need to go back, use the [\'] key"
        )
    
    index.photo = 0
    index.category = 0
    global edgeCase
    edgeCase = EdgeCase.SHOWINGTUTORIAL
    
    