

import os
import DataSortingCategories
from natsort import natsorted


class DataManager():
    #The urls of all the pictures that have been loaded in.
    photoURLs = []

    currentTypeDictionary = None

    def recursiveDictionarySearch(self, dict_ToFind, dict_ToSearch):
        for key in dict_ToSearch.keys():
            if key == dict_ToFind:
                return dict_ToSearch[key]
            elif type(dict_ToSearch[key]) is dict:
                r = self.recursiveDictionarySearch(dict_ToFind, dict_ToSearch[key])
                if r != None:
                    return r
        
        return None

#########

    def folderChosen(self, folderURL):
        #Get all files in the directory
        self.photoURLs = natsorted(os.listdir(folderURL))

        #Add the rest of the filepath to them & cut out any that aren't jpeg
        self.photoURLs = [folderURL + '/' + file for file in self.photoURLs if file.endswith(('.jpeg', '.JPEG', '.jpg', '.JPG'))]

        self.fillDataList(DataSortingCategories.typesToLook4)
        #Initialize the data[] for the first category (top of the data tree) to the correct length. 
        #   The data[] for the other categories will all be created based on the filled out data[] of their parent.
        self.dataList[0]["data"] = [1] * len(self.photoURLs)

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

    def fillDataList(self, dict_OfTypes, parent=None):
        """Recursively fills dataList from a tree-structure nested-dictionary of image trigger types"""
        for key in dict_OfTypes:
            self.dataList.append({'title':key, 'parent': parent, 'data': []})
            if len(dict_OfTypes[key]) > 0:
                self.fillDataList(dict_OfTypes[key], dict_OfTypes)

    def nextType(self):
        currentColumn = next(self.dataIter, None) 

    def checkForSkip(self, photoIndex, categoryIndex):
        """Checks whether the user already answered \"no\" for the parent category."""
        return self.dataList[categoryIndex]['data'][photoIndex] == -1

    #This will hold all the report headers for the final human report
    reportHeaders_Human = ['Corridor', 'Camera', 'Link To File', 'Date', 'Time', 'Note']#Data columns will be appended
    
    #This is a list of all the columns in the final human report. File columns, notes, data columns, etc. Everything.
    reportData_Human = []
    #

    def countPicsInCategory(self, categoryIndex):
        return len(self.dataList[categoryIndex]['data']) - self.dataList[categoryIndex]['data'].count(-1)
