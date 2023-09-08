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
    
    data: list  = field(init=False)
    """1 = Found in photo,
    \n 0 = Not found in photo,
    \n None = Not answered yet,
    \n 'skip' = Parent category not found in photo"""

    def initializeData(self):
        """initializes the category based on the data of the parent category."""
        if None in self.parent.data:
            raise ValueError(self.parent.data, 'parent\'s data is not filled.')
        self.data = [None if x == 1 else 'skip' for x in self.parent.data]

    def getPhotoCounter(self, photoIndex) -> str:
        """Returns the string for the Photo Counter in the UI, ignoring skips."""
        return (
            str(self.__countPhotosSorted(photoIndex) + 1)
            + '/' + 
            str(self.countPhotos())
        )

    def countPhotos(self):
        """Ignores pictures that will be skipped."""
        return len(self.data) - self.data.count('skip')

    def __countPhotosSorted(self, photoIndex):
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
    getCategory(0).data = [None] * len(photoURLs)

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




#######

def flipValueInCategory(categoryIndex):
    category = getCategory(categoryIndex)

    if category.data[index.photo] == 1:
        category.data[index.photo] = 0
        for child in category.children:
            __flipChildrenRecursively(child)
        

    else: #(if 0 or 'skip' or None)
        category.data = 1
        __flipParentsRecursively(category.parent)

        

def __flipChildrenRecursively(category: Category):
    for child in category.children:
            if child.data[index.photo] == 1:
                child.data[index.photo] = 0
                __flipChildrenRecursively(child)

def __flipParentsRecursively(category: Category):
    if category.parent.data[index.photo] != 1:
            category.parent.data[index.photo] = 1
            __flipParentsRecursively(category.parent)

