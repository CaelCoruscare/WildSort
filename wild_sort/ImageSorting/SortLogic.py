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

def recordData(dataValue):
    """Sets data based on the index.photo"""
    category = DataManager.getCategory(index.category)
    category.data[index.photo] = (1 if dataValue == 'yes' else 0)
