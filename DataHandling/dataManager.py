from __future__ import annotations

from dataclasses import dataclass, field
import DataSortingCategories

import DataHandling.ImageExtractor as ImageExtractor


@dataclass
class Index():
    photo: int
    category: int
index = Index(-1,0)

@dataclass
class Category():
    title: str
    parent: Category
    children: list = field(default_factory=lambda: [])
    
    data: list = field(init=False) #This gets filled with [None] during folderInitialization, then filled with useful data when the category is reached
    """1 = Found in photo,
    \n 0 = Not found in photo,
    \n None = Not answered yet,
    \n 'skip' = Parent category not found in photo"""


    def initializeData(self):
        """initializes the category based on the data of the parent category."""
        if self.parent == None:
            self.data = [None] * len(photoURLs)
            return
        if None in self.parent.data:
            raise ValueError(self.parent.data, 'parent\'s data is not filled.')
        
        self.data = [None if x == 1 else 'skip' for x in self.parent.data]

    def getPhotoCounter(self, photoIndex) -> str:
        """Returns the string for the Photo Counter in the UI, ignoring skips."""
        return (
            str(self._countPhotosSorted(photoIndex) + 1)
            + '/' + 
            str(self.countPhotos())
        )

    def countPhotos(self):
        """Ignores pictures that will be skipped."""
        return len(self.data) - self.data.count('skip')

    def _countPhotosSorted(self, photoIndex):
        """Ignores pictures that were skipped. Counts how many pictures the user has sorted for this category."""
        slicedData = self.data[0:photoIndex]
        return len(slicedData) - slicedData.count('skip')

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
          
fillDataList(DataSortingCategories.typesToLook4)

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
        
class FlipValue():
    """
    Flips the value of a category for the current photo.

    \nHandles adjusting other values upstream and downstream.
    """
    def __init__(self, targetCategory: Category):
        self._photoIndex = index.photo
        value = targetCategory.data[index.photo]
        self.DoIt(value, targetCategory)

    def DoIt(self, value, category: Category):
        if value == 1:
            #Parents: No changes

            #Target:
            category.data[index.photo] = 0

            #Children:
            for child in category.children:
                self.setChildAndGrandchildren_ToSkip(child)
            
        elif value == 0: #(if 0 or 'skip' or None)
            #Parents: no changes

            #Target:
            category.data[index.photo] = 1

            #Children:
            for child in category.children:
                self.setChildAndGrandchildren_ToSkip(child)

        elif value == 'skip':
            #Parents:
            self.setParentAndGrandparents_ToOne(category.parent)

            #Target
            category.data[index.photo] = 1

            #Children:
            for child in category.children:
                self.set_ToZero(child)

        elif value == None:
            raise ValueError(value, "UI should prevent flipping a None value.")

    def setParentAndGrandparents_ToOne(self, parent: Category):
        if parent == None:
            return
        parent.data[self._photoIndex] = 1
        self.setParentAndGrandparents_ToOne(parent=parent.parent)

    def set_ToZero(self, category: Category):
        if category.data[index.photo] == None:
            return
        category.data[index.photo] = 0
        
        #Below a 0 is always 'skips' until the Nones start
        for child in category.children:
            self.setChildAndGrandchildren_ToSkip(child=child)

    def setChildAndGrandchildren_ToSkip(self, child: Category):
        if child.data[index.photo] == None:
            return
        child.data[index.photo] = 'skip'
        for grandchild in child.children:
            self.setChildAndGrandchildren_ToSkip(child=grandchild)
