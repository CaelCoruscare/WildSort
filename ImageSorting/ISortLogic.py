from enum import Enum
import os
import time

from DataHandling import DataManager as dataManager

import ImageSorting.CallsToUI as ui
import DataHandling.ReportBuilder as reportBuilder

index = dataManager.Index(-1,0)


smallDelay = 0.2

#index.photo is used to store notes in specific arrays here.
notes = {-1:"You can write notes here when an image is open."}

class EdgeCase(Enum):
    SHOWING_FOLDER_AREA = 0
    SHOWING_CAMERA_AND_LOCATION_FORM = 1
    SHOWING_TUTORIAL = 2
    FIRST_SHOWING_NEXT_CATEGORY = 3
    SHOWING_NEXT_CATEGORY_WILL_BE = 4
    AT_END_OF_CATEGORY = 5
    NONE = 6

edgeCase = EdgeCase.SHOWING_FOLDER_AREA


def __handleAtEndOfCategory(userResponse):
    #-2 is passed in as userResponse if SortLogic is in the process of skipping.
        if userResponse != -2:
            recordData(userResponse)
            ui.flashIcon(userResponse) 

        time.sleep(smallDelay)

        if index.category == len(dataManager.dataList) - 1: #If that was the last category
            ui.set_Photo(None)
            ui.set_Category(None)
            ui.set_PhotoCounter(None)
            ui.showSimple(ui.SimpleElement.DIALOG_PRINT_REPORT)

        else: #Default EndOfCategory behavior 
            ui.set_Category(None)

            nextCategory = dataManager.getCategory(index.category + 1)
            ui.set_NextCategoryWillBe(nextCategory.title)
            nextCategory.initializeData() # Need to do this here so the next line functions
            ui.set_PhotoCounter('-/' + str(nextCategory.countPhotos()))

            global edgeCase
            edgeCase = EdgeCase.SHOWING_NEXT_CATEGORY_WILL_BE
  

    



########## Forward & Back logic
def tryForward(userResponse):
    """Records data, increments the photo index until a non-skip photo is at the index, displays photo after delay"""
    if __handleForwardEdgeCases(userResponse):
        return

    #"-2" allows tryForward() to be called without setting data or flashing an icon.
    if userResponse != -2:
        recordData(userResponse)
        ui.flashIcon(userResponse)

    index.photo +=1

    if index.photo == len(dataManager.photoURLs) - 1:
        global edgeCase
        edgeCase = EdgeCase.AT_END_OF_CATEGORY

    if dataManager.checkForSkip(index):
        tryForward(-2)
    else:
        __forward()

def __forward():
    time.sleep(smallDelay)
    ui.set_Photo(dataManager.getPhoto(index.photo))
    
    currentCategory = dataManager.getCategory(index.category)
    ui.set_PhotoCounter(currentCategory.getPhotoCounter(index.photo))

def __categoryForward():
    """Handles moving the category forward, then calls Forward again"""
    index.category += 1
    ui.set_Category(dataManager.getCategory(index.category).title)

    #Doing this instead of calling setPhoto() because 
    #   tryForward() contains the logic for skipping over unnecessary photos
    index.photo = -1
    tryForward(-2)

def __handleForwardEdgeCases(userResponse):
    global edgeCase

    match edgeCase:
        case EdgeCase.NONE:
            return False
        
        case EdgeCase.SHOWING_FOLDER_AREA: 
            return True #Ignore user input on this screen

        case EdgeCase.AT_END_OF_CATEGORY:
            __handleAtEndOfCategory(userResponse)
            return True
    
    #For cases below this no action should be taken unless user clicked the return/enter key
    if userResponse != 'continue':
        return True

    match edgeCase:
        case EdgeCase.SHOWING_CAMERA_AND_LOCATION_FORM:
            ui.set_CamAndLocForm(None, 'hide this')
            ui.showSimple(ui.SimpleElement.TUTORIAL_KEYS)
            
            edgeCase = EdgeCase.SHOWING_TUTORIAL

            return True

        case EdgeCase.SHOWING_TUTORIAL:
            ui.hideSimple(ui.SimpleElement.TUTORIAL_KEYS)
            ui.set_NextCategoryWillBe('Any Trigger')
            ui.set_PhotoCounter('-/' + str(len(dataManager.photoURLs)))

            edgeCase = EdgeCase.FIRST_SHOWING_NEXT_CATEGORY

            return True
        
        case EdgeCase.FIRST_SHOWING_NEXT_CATEGORY:
            ui.set_NextCategoryWillBe(None)
            ui.set_Category('Any Trigger')
            ui.set_PhotoCounter('1/' +  str(len(dataManager.photoURLs)))
            ui.set_Photo(dataManager.getPhoto(0))

            edgeCase = EdgeCase.NONE

            return True
        
        
        case EdgeCase.SHOWING_NEXT_CATEGORY_WILL_BE:
            ui.set_NextCategoryWillBe(None)

            edgeCase = EdgeCase.NONE

            __categoryForward()
            
            return True
        
        case _:
            raise ValueError(edgeCase, 'No edgeCase match found')


def tryBack():
    if __handleBackEdgeCases():
        return

    index.photo -= 1

    if dataManager.checkForSkip(index):
        tryBack()
    else:
        __back()
        

def __back():
    #Edge cases are handled in tryBack()

    ui.flashIcon('back')
    ui.set_Photo(dataManager.getPhoto(index.photo))

    currentCategory = dataManager.getCategory(index.category)
    ui.set_PhotoCounter(currentCategory.getPhotoCounter(index.photo))

def __categoryBack():
    if index.category == 0:
        return
    
    global edgeCase
    edgeCase = EdgeCase.SHOWING_NEXT_CATEGORY_WILL_BE

    index.category -= 1
    nextCategory = dataManager.getCategory(index.category + 1)
    ui.set_NextCategoryWillBe(nextCategory.title)
    ui.set_PhotoCounter('-/' + str(nextCategory.countPhotos()))
    ui.set_Category(None)
    ui.flashIcon('back')

    index.photo = len(dataManager.photoURLs) - 1

def __handleBackEdgeCases():
    global edgeCase

    if edgeCase == EdgeCase.SHOWING_FOLDER_AREA or edgeCase == EdgeCase.SHOWING_TUTORIAL or edgeCase == EdgeCase.FIRST_SHOWING_NEXT_CATEGORY:
        return True #Ignore user input before sorting starts

    if edgeCase == EdgeCase.AT_END_OF_CATEGORY:
        edgeCase = EdgeCase.NONE
        tryBack()
        return True

    if edgeCase == EdgeCase.SHOWING_NEXT_CATEGORY_WILL_BE:
        edgeCase = EdgeCase.AT_END_OF_CATEGORY
        ui.set_NextCategoryWillBe(None)
        ui.set_Category(dataManager.getCategory(index.category).title)

        #This is to avoid hitting handleBackEdgeCases() again
        __back()
        if dataManager.checkForSkip(index):
            tryBack()

        return True
    
    if index.photo == 0:
        __categoryBack()
        return True

    return False



#########Supporting Functions

def recordData(dataValue):
    """Sets data based on the index.photo"""
    if index.photo < len(dataManager.photoURLs) and index.photo > -1: #Skip if we are on a blank screen between categories
        dataManager.getCategory(index.category).data[index.photo] = dataValue

###Pass-Alongs--------
#TODO: I think it may be best to remove any of these that do not directly impact Sort Logic

def folderChosen(folderURL):
    #Datamanager handles the data
    dataManager.folderChosen(folderURL)

    index.photo = 0
    index.category = 0

    camera = os.path.basename(folderURL) # Camera name is assumed to be the name of the folder
    ui.set_CamAndLocForm(str(camera), reportBuilder.location)

    reportBuilder.folderOfPhotos = folderURL

    global edgeCase
    edgeCase = EdgeCase.SHOWING_CAMERA_AND_LOCATION_FORM

def setCameraAndLocation(camera, location):
    reportBuilder.camera = camera
    reportBuilder.location = location

def setNote(text):
    #TODO: I think notes when there's no pictures is now fully handled by the QML file just not calling for notes when a picture is not showing. Should double check and maybe clean it up
    if edgeCase == EdgeCase.NONE or edgeCase == EdgeCase.AT_END_OF_CATEGORY: 
        dataManager.setNote(index.photo, text)
    else:
        dataManager.setNote(-1, text)
        
def getNote():
    #TODO: I think notes when there's no pictures is now fully handled by the QML file just not calling for notes when a picture is not showing. Should double check and maybe clean it up
    if edgeCase == EdgeCase.NONE or edgeCase == EdgeCase.AT_END_OF_CATEGORY:
        return dataManager.getNote(index.photo)
    else:
        return dataManager.getNote(-1)
    
def writeReport():
    reportBuilder.buildReports_Human(dataManager.dataList, dataManager.photoURLs, dataManager.notes)
    