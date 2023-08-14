from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtCore import QObject, Signal, Property
from natsort import natsorted

import datetime
from datetime import datetime

import os

import csv
import exifread

from DataHandling.dataManager import dataManager
from DataHandling.reportBuilder import reportBuilder

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class ImageLogic(QObject):

    picIndex = -1
    typeIndex = 0

    looking4Changed = Signal(str)
    pictureChanged = Signal(str)
    flashIcon = Signal(str)

    typesList = [] 
    #typesList[] contains not only the list of different Types to sort animals into, but also 
    #   commands for where to place each type on the data tree
    #ie ["Any Trigger", "_down_", "Human", "_down_", "On Foot", "Vehicle", "_up_", "Wild Animal", "_up_", "_end_"] 
    #   would produce a tree like so:
    #
    #            "Any Trigger"
    #                  |
    #               /     \
    #         "Human"   "Wild Animal"
    #           |           
    #        /     \
    # "On Foot"  "Vehicle"



    

    #currentPicIndex is used to store notes in specific arrays here.
    notes = {-1:"You can write notes here when an image is open."}

    #This just handles initialization
    def __init__(self):
        QObject.__init__(self)
        print("")
        print("")
        print("")
        #self.writeReport()

    
    
    
    def recursiveGetAllNamesAndData(self, d, listHeader, listData):
        for key in d.keys():
            if key != "data" and key != "subcolumns":
                listHeader.append(d[key])
                listData.append(d[key]['data']) 
                for subcolumn in d[key]['subcolumns']:
                    self.recursiveGetAllNamesAndData


##########

    def isOnBlankScreen(self):
        """Returns true if on the blank screen between categories or the blank screen at the end with the [Print Report] button"""
        return self.photoIndex == len(dataManager.photoURLs)

    def photoForward(self):
        """increments the photo index and handles all resulting logic"""
        self.photoIndex +=1

        if self.isOnBlankScreen():
            self.show_NextCategoryWillBe()

        elif self.photoIndex > len(dataManager.photoURLs):
            self.categoryForward() 

        elif dataManager.checkForSkip(self.photoIndex, self.categoryIndex):
            self.photoForward()
            pass

        else:
            self.showPhoto()
            

    def photoBack(self):
        self.photoIndex -= 1
        if self.photoIndex == -1:
            self.categoryBack()
        else:
            self.showPhoto()

    def categoryForward(self):
        self.categoryIndex += 1
        if self.categoryIndex == len(dataManager.dataList):
            self.show_AreYouReadyToPrintReport_Button() #Last chance before writing report
        elif self.categoryIndex < len(dataManager.dataList):
            self.photoIndex = 0
            self.showPhoto()

    def categoryBack(self):
        if self.categoryIndex > 0:
            self.categoryIndex -=1
            self.photoIndex = len(dataManager.photoURLs)
            self.flashIcon.emit("back")
            self.show_NextCategoryWillBe()

    def showPhoto(self):
        #TODO: Add a delay of 0.2 seconds
        self.pictureChanged(dataManager.photoURLs[self.photoIndex], str(self.photoIndex) + '/' + str(len(dataManager.photoURLs)))
    
    def show_NextCategoryWillBe(self):
        #TODO: Add a delay of 0.2 seconds
        self.pictureChanged('AppImages/restart-arrow.png', '')

    def show_AreYouReadyToPrintReport_Button(self):
        #TODO: Add a delay of 0.2 seconds
        self.pictureChanged('','')


###########
    
    
    
    
    #Uses a JSON to fill the TypesList which will be used to keep track of what the program is looking for.
    #   The JSON will eventually be pulled from a file, which can be edited by a user during set-up to customize categories.
    def fillTypesList(self, dict_OfTypes, list_ToFill):
        for type in dict_OfTypes:
            list_ToFill.append(type)
            if len(dict_OfTypes[type]) > 0:
                list_ToFill.append("_down_")
                self.fillTypesList(dict_OfTypes[type], list_ToFill)
                list_ToFill.append("_up_")
    
    def getNextCommandOrType(self):
        self.typeIndex = self.typeIndex + 1
        typeOrCommand = self.typesList[self.typeIndex]
        return typeOrCommand
    
    
    def recordData(self, dataValue):
        """Sets data based on the picIndex"""
        if self.photoIndex < len(dataManager.photoURLs): #Skip if we are on a blank screen between categories, or on the PrintReport page
            dataManager.currentTypeDictionary['data'][self.picIndex] = dataValue

    #This covers all aspects of finishing up data collection for a Type, 
    #   setting up for the next Type, 
    #   and returns the str of next Type
    def moveToNextType(self):
        #reset the pic index so the pictures start from the beginning
        self.picIndex = -1

        #The Type List has the types but also commands of "_up_", "_down_", or "_end_", which need to be processed.
        typeOrCommand = self.getNextCommandOrType()
        match typeOrCommand:
            case "_down_":
                #Get the current dict in the allData nested dict
                current = dataManager.recursiveDictionarySearch(dataManager.typeAddress[-1], dataManager.dataTree)

                #Get the Type that is after the "_down_" command
                typeAfterCommand = self.getNextCommandOrType()

                #Create the new section of the allData nested dict
                current['subcolumns'][typeAfterCommand] = {"data": current['data'].copy(), "subcolumns":{}}

                #Update the typeAddress to point to the new part of the allData nested dict
                dataManager.typeAddress.append(typeAfterCommand)
            case "_up_":
                #pop() once to get up to the current level (equivalent to making a subcolumn at the current level)
                dataManager.typeAddress.pop()
                #Go up as many times as there are consecutive "_up_" in typeList, 
                #   popping the address each time, 
                #   and increasing the typeList index until getNextCommandOrType() returns a type
                command = typeOrCommand
                while command == "_up_":
                    dataManager.typeAddress.pop()
                    command = self.getNextCommandOrType() 

                #Get the Type that is after the 1 or more "_up_" commands
                if command == "_end_":
                    self.writeReport()
                    reportBuilder.writeReport_Human()
                else:
                    typeAfterCommands = command

                #Get the current dict in the allData nested dict
                dataManager.updateCurrentTypeDictionary()
                parentOrGrandparent = dataManager.currentTypeDictionary

                #Create the new section of the data JSON
                parentOrGrandparent['subcolumns'][typeAfterCommands] = {"data": parentOrGrandparent['data'].copy(), "subcolumns":{}}

                #Update the typeAddress to point to the new part of the allData nested dict
                dataManager.typeAddress.append(typeAfterCommands)
            case "_end_":
                raise NotImplementedError("_end_ should only be after 1 or more _up_s, so this should not be hit", self.typesList)
            case _:
                #Update the typeAddress to point to the parent, since the new Type will be a subcolumn of the parent
                dataManager.typeAddress.pop()
                parent = dataManager.updateCurrentTypeDictionary()

                #Create the new section of the allData nested dict
                parent['subcolumns'][typeOrCommand] = {"data": parent['data'].copy(), "subcolumns":{}}

                #Update the typeAddress to point to the new part of the allData nested dict
                dataManager.typeAddress.append(typeOrCommand)

        #Sets the data array for when data is collected
        dataManager.updateCurrentTypeDictionary()

            

        #Tell the UI to update the "Is there a ____?" area
        self.looking4Changed.emit(dataManager.typeAddress[-1])

        #Flash the Typechange Icon on screen so the user knows that we are changing types
        self.flashIcon.emit("typechange")

        self.getNextPhoto()

    def getNextPhoto(self):
        """Move through the pics until hitting the next one that is relevant for the current Type
        
        i.e. If the current Type is "Camel", it skips all photos where "Domestic Animal" was answered no
        This works because the data for "Domestic Animal" was used to create the data ofr "Camel".
        """
        currentTypeData = dataManager.currentTypeDictionary['data']
        self.picIndex += 1
        try:
            while currentTypeData[self.picIndex] == 2:
                self.picIndex += 1
        except IndexError as error:
            self.moveToNextType()

        
            
        #Fetch the picture URL and pass it back
        nextPicURL = dataManager.photoURLs[self.picIndex]
        return nextPicURL
    
    def getLastPhoto(self):
        if self.picIndex == 0:
            #Going back to the last Type is going to require a special handling case
            print("Have not implemented going back to the last Type yet.")
        else:
            self.picIndex -=1

            return dataManager.photoURLs[self.picIndex]
    

    #Accept a folder URL, return the URL of the first picture in the list of pics in the folder.
    @Slot(str, result=str)
    def setFolder(self, folderURL):
        #Fix for QT Filepath:  
        #   file:///Users/test/Pictures --> /Users/test/Pictures
        folderURLFixed = folderURL[7:]

        #Get all files in the directory
        dataManager.photoURLs = natsorted(os.listdir(folderURLFixed))

        #Add the rest of the filepath to them & cut out any that aren't jpeg
        dataManager.photoURLs = [folderURLFixed + '/' + file for file in dataManager.photoURLs if file.endswith(('.jpeg', '.JPEG', '.jpg', '.JPG'))]

        #Set the "Any Trigger" data list to be a number of 1s equal to the number of pictures.
        #   In a data list, a 1 that has not been accessed yet means that it needs to be checked.
        #   This is because the data list is passed down the allData dict tree from parent to children, to keep track of which pictures do not need to be checked for a Type
        #   Because if there is no "Domestic Animal" trigger, then there is no point asking if there is a "Donkey" trigger
        dataManager.dataTree["Any Trigger"]["data"] = [1] * len(dataManager.photoURLs)

        #Set the UI to "Is there: Any Trigger?"
        self.looking4Changed.emit(dataManager.typeAddress[-1])
        self.pictureChanged.emit('0' + "/" + str(len(dataManager.photoURLs)))

        #TESTING
        #fileData = []
        #self.getFileData(dataManager.pictureURLs, fileData)
        #TESTING
        
        #Make sure the pictures start from the beginning 
        #   (for once opening multiple folders is implemented)
        self.picIndex = -1

        #Set the data array for the current type.
        self.currentDataArray = dataManager.recursiveDictionarySearch(dataManager.typeAddress[-1], dataManager.dataTree)

        return self.getNextPhoto()
     
    @Slot(str)
    def choiceMade(self, choice):
        #Make sure the list of pictures has been initialized.
        if not dataManager.photoURLs:
            raise ValueError("pictureURLs List has not been initialized.", dataManager.photoURLs)

        #Update or roll back any data, then get the url for the picture that should be shown.        
        picToShow = "I'm A File URL"
        match choice.lower():
            case "yes":
                if not self.isOnBlankScreen():
                    self.flashIcon.emit("yes")
                    self.recordData(1)
                ###
                self.photoForward()
                
            case "no":
                if not self.isOnBlankScreen():
                    self.flashIcon.emit("yes")
                    self.recordData(0)
                ###
                self.photoForward()

            case "back":
                ###
                self.photoBack()

            case _:
                raise ValueError("user choice passed in is not valid. Should be \'yes\',\'no\', or \'back\' (case insensitive)" , choice)

        return picToShow
    
    @Slot(str)
    def recordNote(self, note):
        print(note)
        self.notes[self.picIndex] = note

    @Slot(result=str)
    def getNote(self):
        return self.notes.get(self.picIndex, "")
    