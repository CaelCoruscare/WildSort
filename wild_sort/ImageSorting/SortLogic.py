from enum import Enum
import os
import time

from DataHandling import DataManager
from DataHandling.DataManager import index

import ImageSorting.CallsToUI as ui

from WildElements.WildElement import WildElement
from WildElements import WildScreens as Screens
photoElement = WildElement('photo')

smallDelay = 0.05

def choiceMade(yesOrNo):
    recordData(yesOrNo)
    time.sleep(smallDelay)
    nextPhoto()
    
def nextPhoto():
    """Moves to the next photo, skipping photos that are ruled out for the current category, and telling the ScreenManager \"next()\" when all photos in the current category are accounted for. """
    index.photo +=1
    
    while index.photo <= index.photoMax():
        if DataManager.checkForSkip(index):
            index.photo +=1
        else:
            photoElement.set(DataManager.getPhotoURL(index.photo))
            return
        
    #Go to NextCategory screen or PrintReport screen
    Screens.screenManager.next() 

def previousPhoto():
    index.photo -=1

    while index.photo > -1:
        if DataManager.checkForSkip(index):
            index.photo -=1
        else: 
            photoElement.set(DataManager.getPhotoURL(index.photo))
            return

    Screens.screenManager.back()

def _back():
    #Edge cases are handled in tryBack()

    ui.flashIcon('back')
    ui.set_Photo(DataManager.getPhotoURL(index.photo))

    currentCategory = DataManager.getCategory(index.category)
    ui.set_PhotoCounter(currentCategory.getPhotoCounter(index.photo))

def _categoryBack():
    if index.category == 0:
        return
    
    global edgeCase
    edgeCase = EdgeCase.SHOWING_NEXT_CATEGORY_WILL_BE

    index.category -= 1
    nextCategory = DataManager.getCategory(index.category + 1)
    ui.set_NextCategoryWillBe(nextCategory.title)
    ui.set_PhotoCounter('-/' + str(nextCategory.countPhotos()))
    ui.set_Category(None)
    ui.flashIcon('back')

    index.photo = len(DataManager.photoURLs) - 1

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
        ui.set_Category(DataManager.getCategory(index.category).title)

        #This is to avoid hitting handleBackEdgeCases() again
        if DataManager.checkForSkip(index):
            tryBack()
        else:
            _back()

        return True
    
    if index.photo == 0:
        _categoryBack()
        return True

    return False

def recordData(dataValue):
    """Sets data based on the index.photo"""
    category = DataManager.getCategory(index.category)
    category.data[index.photo] = (1 if dataValue == 'yes' else 0)
