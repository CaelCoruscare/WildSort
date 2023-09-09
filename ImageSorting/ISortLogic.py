from enum import Enum
import os
import time

from DataHandling import DataManager as dataManager

import ImageSorting.CallsToUI as ui
from ImageSorting.CallsToUI import Screen

import DataHandling.ReportBuilder as reportBuilder

index = dataManager.index


smallDelay = 0.05

#index.photo is used to store notes in specific arrays here.
notes = {-1:"You can write notes here when an image is open."}

class EdgeCase(Enum):
    SHOWING_FOLDER_AREA = 0
    SHOWING_CAMERA_AND_LOCATION_FORM = 1
    SHOWING_TUTORIAL_KEYS = 2
    SHOWING_TUTORIAL_CATEGORIES = 3
    SHOWING_TUTORIAL_IMAGES = 4
    FIRST_SHOWING_NEXT_CATEGORY = 5
    SHOWING_NEXT_CATEGORY_WILL_BE = 6
    AT_END_OF_CATEGORY = 7
    NONE = 8

edgeCase = EdgeCase.SHOWING_FOLDER_AREA


def _handleAtEndOfCategory(userResponse):
    #-2 is passed in as userResponse if SortLogic is in the process of skipping.
        if userResponse != -2:
            recordData(userResponse)
            ui.flashIcon(userResponse) 

        time.sleep(smallDelay)

        if index.category == len(dataManager.dataList) - 1: #If that was the last category
            ui.set_Photo(None)
            ui.set_Category(None)
            ui.set_PhotoCounter(None)
            ui.showScreen(Screen.SCREEN_PRINT_REPORT)

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
    if _handleForwardEdgeCases(userResponse):
        return
    
    #"Continue" userResponse should be ignored if there is no edge case to handle
    if userResponse == "continue":
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

def _categoryForward():
    """Handles moving the category forward, then calls Forward again"""
    index.category += 1
    ui.set_Category(dataManager.getCategory(index.category).title)

    #Doing this instead of calling setPhoto() because 
    #   tryForward() contains the logic for skipping over unnecessary photos
    index.photo = -1
    tryForward(-2)

def _handleForwardEdgeCases(userResponse) -> bool:
    """Returns true if there was an edge case, else false if normal logic should apply."""
    global edgeCase

    match edgeCase:
        case EdgeCase.NONE:
            return False
        
        case EdgeCase.SHOWING_FOLDER_AREA: 
            return True #Ignore user input on this screen

        case EdgeCase.AT_END_OF_CATEGORY:
            _handleAtEndOfCategory(userResponse)
            return True
    
    #For cases below this no action should be taken unless user clicked the return/enter key
    if userResponse != 'continue':
        return True

    match edgeCase:
        case EdgeCase.SHOWING_CAMERA_AND_LOCATION_FORM:
            #Hide UI
            ui.hideScreen(Screen.SCREEN_CAMERA_LOCATION)
            #Show UI
            ui.showScreen(Screen.TUTORIAL_KEYS)
            #Update Edge Case
            edgeCase = EdgeCase.SHOWING_TUTORIAL_KEYS

            return True

        case EdgeCase.SHOWING_TUTORIAL_KEYS:
            #Hide UI
            ui.hideScreen(ui.Screen.TUTORIAL_KEYS)
            #Show UI
            ui.set_NextCategoryWillBe(dataManager.getCategory(0).title)
            ui.set_PhotoCounter('-/' + str(len(dataManager.photoURLs)))
            #Update Edge Case
            edgeCase = EdgeCase.FIRST_SHOWING_NEXT_CATEGORY

            return True

        #TODO: IMPLEMENT
        case EdgeCase.SHOWING_TUTORIAL_CATEGORIES: 
            #Hide UI
            ui.hideScreen(Screen.TUTORIAL_CATEGORIES)
            #Show UI
            ui.set_NextCategoryWillBe(dataManager.getCategory(0).title)
            ui.set_PhotoCounter('-/' + str(len(dataManager.photoURLs)))
            #Update Edge Case
            edgeCase = EdgeCase.FIRST_SHOWING_NEXT_CATEGORY

            return True
        
        case EdgeCase.FIRST_SHOWING_NEXT_CATEGORY:
            #Hide UI
            ui.set_NextCategoryWillBe(None)
            #Show UI
            ui.set_Category(dataManager.getCategory(0).title)
            ui.set_PhotoCounter('1/' +  str(len(dataManager.photoURLs)))
            ui.set_Photo(dataManager.getPhoto(0))
            #Update Edge Case
            edgeCase = EdgeCase.NONE

            return True
        
        
        case EdgeCase.SHOWING_NEXT_CATEGORY_WILL_BE:
            ui.set_NextCategoryWillBe(None)

            edgeCase = EdgeCase.NONE

            _categoryForward()
            
            return True
        
        case _:
            raise ValueError(edgeCase, 'No edgeCase match found')


def tryBack():
    if _handleBackEdgeCases():
        return

    index.photo -= 1

    if dataManager.checkForSkip(index):
        tryBack()
    else:
        _back()
        

def _back():
    #Edge cases are handled in tryBack()

    ui.flashIcon('back')
    ui.set_Photo(dataManager.getPhoto(index.photo))

    currentCategory = dataManager.getCategory(index.category)
    ui.set_PhotoCounter(currentCategory.getPhotoCounter(index.photo))

def _categoryBack():
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

def _handleBackEdgeCases():
    global edgeCase

    if edgeCase == EdgeCase.SHOWING_FOLDER_AREA or edgeCase == EdgeCase.SHOWING_TUTORIAL_KEYS or edgeCase == EdgeCase.FIRST_SHOWING_NEXT_CATEGORY:
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
        if dataManager.checkForSkip(index):
            tryBack()
        else:
            _back()

        return True
    
    if index.photo == 0:
        _categoryBack()
        return True

    return False



#########Supporting Functions

def recordData(dataValue):
    """Sets data based on the index.photo"""
    if edgeCase == EdgeCase.NONE or edgeCase == EdgeCase.AT_END_OF_CATEGORY:
        dataManager.getCategory(index.category).data[index.photo] = dataValue
    else:
        raise ValueError(edgeCase, "Should not be trying to record data if not on a photo screen.")

###Pass-Alongs--------
#TODO: I think it may be best to remove any of these that do not directly impact Sort Logic

def folderChosen(folderURL):
    #Datamanager handles the data
    dataManager.initializeFromFolder(folderURL)

    #This is for the Notes popup
    listOfTitles = [category.title for category in dataManager.dataList]
    ui.createCategoryCheckboxes(listOfTitles)

    #UI Hide
    ui.hideScreen(Screen.SCREEN_LOAD_FOLDER)

    #UI Show
    camera = str( os.path.basename(folderURL) ) # Camera name is assumed to be the name of the folder
    location = reportBuilder.location # Location is assumed to be the same as the last time a folder was opened (currently has no memeory between runs)
    ui.set_CamAndLocForm(camera, location)
    ui.showScreen(ui.Screen.SCREEN_CAMERA_LOCATION)

    reportBuilder.folderOfPhotos = folderURL

    global edgeCase
    edgeCase = EdgeCase.SHOWING_CAMERA_AND_LOCATION_FORM

def setCameraAndLocation(camera, location):
    reportBuilder.camera = camera
    reportBuilder.location = location

def setNote(text):
    if edgeCase == EdgeCase.NONE or edgeCase == EdgeCase.AT_END_OF_CATEGORY: 
        dataManager.setNote(index.photo, text)
    else:
        dataManager.setNote(-1, text)
        
def getNote():
    if edgeCase == EdgeCase.NONE or edgeCase == EdgeCase.AT_END_OF_CATEGORY:
        return dataManager.getNote(index.photo)
    elif edgeCase == EdgeCase.SHOWING_TUTORIAL_KEYS:
        return dataManager.getNote(-1) 
    else:
        return "NULL" #TODO: Need to figure out the Python -> QML way to handle passing None/NULL
    
def writeReport():
    reportBuilder.buildReports_Human(dataManager.dataList, dataManager.photoURLs, dataManager.notes)
    ui.showScreen(Screen.SCREEN_LOAD_FOLDER)
    

def setCategoriesScreen():
    for category in dataManager.dataList:
        category.title