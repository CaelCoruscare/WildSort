from dataclasses import dataclass
import os
import DataSortingCategories
from natsort import natsorted
from types import SimpleNamespace

@dataclass
class Index():
    photo: int
    category: int

#The urls of all the pictures that have been loaded in.
photoURLs = []

def recursiveDictionarySearch( dict_ToFind, dict_ToSearch):
    for key in dict_ToSearch.keys():
        if key == dict_ToFind:
            return dict_ToSearch[key]
        elif type(dict_ToSearch[key]) is dict:
            r = recursiveDictionarySearch(dict_ToFind, dict_ToSearch[key])
            if r != None:
                return r
    
    return None

#########

def folderChosen(folderURL):
    #Get all files in the directory
    global photoURLs
    photoURLs = natsorted(os.listdir(folderURL))

    #Add the rest of the filepath to them & cut out any that aren't jpeg
    photoURLs = [folderURL + '/' + file for file in photoURLs if file.endswith(('.jpeg', '.JPEG', '.jpg', '.JPG'))]

    fillDataList(DataSortingCategories.typesToLook4)
    #Initialize the data[] for the first category (top of the data tree) to the correct length. 
    #   The data[] for the other categories will all be created based on the filled out data[] of their parent.
    dataList[0]["data"] = [1] * len(photoURLs)

dataList = []
"""
Holds data on which pictures each type appears in. \n
1='in picture' , 0='not in picture' , -1='parent type not in picture, so don't need to check'\n
Example: 
    [{'type':'any', 'parent': None,     'data': [0,1,0,0,1,1]}, \n
    {'type':'domestic', 'parent': *any, 'data': [-1,0,-1,-1,1,0]}, \n
    {'type':'wild', 'parent': *any,     'data': [-1,1,-1,-1,0,1]} \n
    {'type':'cheetah', 'parent': *wild, 'data': [-1,0,-1,-1,-1,1]}]
"""

def fillDataList(dict_OfTypes, parent=None):
    """Recursively fills dataList from a tree-structure nested-dictionary of image trigger types"""
    for key in dict_OfTypes:
        dataList.append({'title':key, 'parent': parent, 'data': []})
        if len(dict_OfTypes[key]) > 0:
            fillDataList(dict_OfTypes[key], dataList[-1])

            
def findSkipsFromParentData(categoryIndex):
    """By copying the parent's data and setting each \"NO\" in the parent's data as a \"-1\" in the child's data, we allow skipping those."""
    parentList = dataList[categoryIndex]['parent']['data']
    newData = [x if x == 1 else -1 for x in parentList]
    dataList[categoryIndex]['data'] = newData

def checkForSkip(index: Index):
    """Checks whether the user already answered \"no\" for the parent category."""
    return dataList[index.category]['data'][index.photo] == -1

def getCategoryTitle(categoryIndex):
    return dataList[categoryIndex]['title']

def getPhoto(photoIndex):
    return photoURLs[photoIndex]

###For Updating Photo Counter in UI
def countPhotosInCategory(categoryIndex):
    """Ignores pictures that will be skipped."""
    return len(dataList[categoryIndex]['data']) - dataList[categoryIndex]['data'].count(-1)

def countPicsAsked(index: Index):
    """Ignores pictures that were skipped. Counts how many pictures the user has answered."""
    slicedData = dataList[index.category]['data'][0:index.photo]
    return len(slicedData) - slicedData.count(-1) + 1
#######
