

import csv
from datetime import datetime
import exifread


class dataManager():
    #The urls of all the pictures that have been loaded in.
    photoURLs = []

    #data is the JSON where the data will be stored pending the building of a report. 
    #This shows the structure of the eventual JSON, which keeps a tree structure so that data can be easily copied downwards,
    #   because when a Type is a child of a parent Type, all "NO" answers in the data should be passed down as well.
    #   i.e. if the picture does not contain a "Domestic Animal", then it also will not contain a "Donkey",
    #   So we only need to ask the User "is there a Donkey?" for any pictures where "is there a Domestic Animal?" was answered yes.
    dataTree = {
        "Any Trigger": {
            "data": [0,1,0,0,0,1]
            ,"subcolumns": {

            }
        }
    }

    typeAddress = ['Any Trigger']
    #typeAddress is the address of the current Type, in the Data dictionary,
    #   stored as a set of strings so that all parents are tracked
    #   i.e. ["Any Trigger", "Domestic", "Camel"] -> AnyTrigger.Domestic.Camel

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

    dataList = []
    """
    Holds data on which pictures each type appears in. \n
    1='in picture' , 0='not in picture' , 2='parent type not in picture (don't need to check)'\n
    Example: 
        [{'type':'any', 'parent': None, 'data': [0,1,0,0,1,1]}, \n
        {'type':'domestic', 'parent': *any, 'data': [2,0,2,2,1,0]}, \n
        {'type':'wild', 'parent': *any, 'data': [2,1,2,2,0,1]} \n
        {'type':'cheetah', 'parent': *wild, 'data': [2,0,2,2,2,1]}]
    """
    dataIter = iter(dataList)
    def fillDataList(self, dict_OfTypes, parent=None):
        """Recursively fills dataList from a tree-structure nested-dictionary of image trigger types"""
        for key in dict_OfTypes:
            self.dataList.append({'title':key, 'parent': parent, 'data': []})
            if len(dict_OfTypes[key]) > 0:
                self.fillTypesList(dict_OfTypes[key], dict_OfTypes)

    def nextType(self):
        currentColumn = next(self.dataIter, None) 

    def checkForSkip(self, photoIndex, categoryIndex):
        """Checks whether the user already answered \"no\" for the parent category."""
        return self.dataList[categoryIndex]['data'][photoIndex] == 2

    #This will hold all the report headers for the final human report
    reportHeaders_Human = ['Corridor', 'Camera', 'Link To File', 'Date', 'Time', 'Note']#Data columns will be appended
    
    #This is a list of all the columns in the final human report. File columns, notes, data columns, etc. Everything.
    reportData_Human = []
    #
