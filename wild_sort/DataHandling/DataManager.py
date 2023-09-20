from __future__ import annotations

from dataclasses import dataclass
import DataSortingCategories

import DataHandling.ImageExtractor as ImageExtractor

from DataHandling.Category import Category
from DataHandling.FlipValue import FlipValue


@dataclass
class Index():
    photo: int
    category: int
index = Index(-1,0)

###Photos

photoURLs = list[str]
    
def initializeFromFolder(folderURL):
    global photoURLs
    photoURLs = ImageExtractor.getImages(folderURL)

    #Initialize the data[] for the first category (top of the data tree) to the correct length. 
    #   The data[] for the other categories will all be created based on the filled out data[] of their parent.
    for category in dataList:
        category.data = [None] * len(photoURLs)

    index.photo = 0
    index.category = 0


def getPhoto(photoIndex):
    return photoURLs[photoIndex]


###----------------------------------


###Data
dataList = [] #type: list[Category]
"""Holds data on which pictures each category appears in."""

def fillDataList(dict_OfTypes, parent=None):
    """Recursively fills dataList from a tree-structure nested-dictionary of image trigger types"""
    for key in dict_OfTypes:
        dataList.append((Category(title=key, parent=parent)))
        
        if len(dict_OfTypes[key]) > 0:
            fillDataList(dict_OfTypes[key], dataList[-1])
          
fillDataList(DataSortingCategories.typesToLook4Full)

for category in dataList:
    if category.parent != None:
        category.parent.children.append(category)

###

def getCategory(categoryIndex)->Category:
    return dataList[categoryIndex]

def checkForSkip(index: Index):
    """Checks whether the user already answered \"no\" for the parent category."""
    return getCategory(index.category).data[index.photo] == 'skip'

###----------------------------


###Notes

notes = {-1:"You can put notes here when a picture is loaded."}

def setNote(photoIndex, note):
    notes[photoIndex] = note

def getNote(photoIndex):
    return notes.get(photoIndex, "")


###----------------------------


def getPhotoData():
    photoData = []

    for category in dataList:
        photoData.append(category.data[index.photo])

    return photoData

#######



def flipValueInCategory(categoryIndex):
    category = getCategory(categoryIndex)
    flipper = FlipValue(category, photoIndex=index.photo)
        