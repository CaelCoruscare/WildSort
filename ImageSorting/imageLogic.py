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

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "io.qt.textproperties"
QML_IMPORT_MAJOR_VERSION = 1


@QmlElement
class ImageLogic(QObject):

    pictureURLs = []
    picIndex = -1
    typeIndex = 0

    looking4Changed = Signal(str)
    pictureChanged = Signal(str)
    flashIcon = Signal(str)

    typesToLook4 = {
        'Any Trigger': {
            'Human Elements': { 
                'People':{}
                ,'Motorbikes':{}
                ,'Cars':{}
            }, 
            'Domestic Animals': { 
                'Shoats':{}
                ,'Camels':{}
                ,'Donkeys':{}
                ,'Cattle':{}
                ,'Domestic Dogs':{}
            },
            'Wild Animals': {
            }
        }
    }
    typesToLook4Full = {'Human Stuff': { 
                        'Humans on Foot':{}
                        ,'Motorbikes':{}
                        ,'Cars':{}
                        }, 
                    'Domestic Animals': { 
                        'Shoats':{}
                        ,'Camels':{}
                        ,'Donkeys':{}
                        ,'Domestic Dogs':{}
                        },
                    'Wild Animals': {
                        'Predators':{
                            'Cats':{}
                            ,'Hyenas':{}
                            ,'Painted Dogs':{}
                            ,'Baboons':{}
                            }
                        ,'Herbivores':{
                            'Zebras':{}
                            ,'Antelopes':{}
                            ,'Elephants':{}
                            ,'Hyrax':{}
                            }
                        ,'Omnivores': {
                            'Fox':{}
                            ,'Genet':{}
                            ,'Mongoose':{}
                            ,'BushBaby':{}
                            }
                        ,'Birds':{}
                        }}
    

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


    #data is the JSON where the data will be stored pending the building of a report. 
    #This shows the structure of the eventual JSON, which keeps a tree structure so that data can be easily copied downwards,
    #   because when a Type is a child of a parent Type, all "NO" answers in the data should be passed down as well.
    #   i.e. if the picture does not contain a "Domestic Animal", then it also will not contain a "Donkey",
    #   So we only need to ask the User "is there a Donkey?" for any pictures where "is there a Domestic Animal?" was answered yes.
    allData = {
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

    #currentPicIndex is used to store notes in specific arrays here.
    notes = {-1:"You can write notes here when an image is open."}

    #This just handles initialization
    def __init__(self):
        QObject.__init__(self)
        self.fillTypesList(self.typesToLook4, self.typesList)
        self.typesList.append("_end_")
        print("")
        print("")
        print(self.typesList)
        print("")
        print("")
        print("")
        #self.writeReport()

    def recursiveDictSearch(self, d, keyToFind):
        for key in d.keys():
            if key == keyToFind:
                return d[key]
            elif type(d[key]) is dict:
                r = self.recursiveDictSearch(d[key], keyToFind)
                if r != None:
                    return r
        
        return None

    #Uses typeAddress to find the corresponding dict in allData
    def getCurrentDict_InAllData(self):
        currentDictionary = self.recursiveDictSearch(self.allData, self.typeAddress[-1])
        return currentDictionary
    
    def recursiveGetAllNamesAndData(self, d, listHeader, listData):
        for key in d.keys():
            if key != "data" and key != "subcolumns":
                listHeader.append(d[key])
                listData.append(d[key]['data']) 
                for subcolumn in d[key]['subcolumns']:
                    self.recursiveGetAllNamesAndData

    def getFileData(self, pictureURLs, fileData):
        for url in pictureURLs:
            #Link To File
            linkToFile = url,


            with open(url, 'rb') as fh:
                tags = exifread.process_file(fh)
                datetimeTaken = tags["EXIF DateTimeOriginal"]
                subsecTimeTaken = tags.get("EXIF SubsecTimeOriginal")
                #2003:08:11 16:45:32
            datetime_obj = datetime.strptime(datetimeTaken, "%Y:%m:%d %H:%M:%S")

            if subsecTimeTaken is not None:
                datetime_obj = datetime_obj + subsecTimeTaken
            #Date Taken
            dateTaken = datetime_obj.date()

            #Time Taken
            timeTaken = datetime_obj.time()

            #Transect	Camera	File	Date	Time
            fileData.append(
                linkToFile, 
                dateTaken,
                timeTaken
            )

    def writeReport(self):
        headers = ['Link To File', 'Camera', 'Photo Number', 'Date', 'Time', 'Notes']

        sortData = []
        #self.recursiveGetAllNamesAndData(self.allData, headers, sortData)
        #zip(sortData)

        fileData = []
        self.getFileData(self.pictureURLs, fileData)

        with open('countries.csv', 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the header
            writer.writerow(header)

            # write multiple rows
            writer.writerows(data)

    
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
    
    def updateCurrentData(self, dataValue):
        current = self.getCurrentDict_InAllData()
        current['data'][self.picIndex] = dataValue

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
                current = self.getCurrentDict_InAllData()

                #Get the Type that is after the "_down_" command
                typeAfterCommand = self.getNextCommandOrType()

                #Create the new section of the allData nested dict
                current['subcolumns'][typeAfterCommand] = {"data": current['data'].copy(), "subcolumns":{}}

                #Update the typeAddress to point to the new part of the allData nested dict
                self.typeAddress.append(typeAfterCommand)
            case "_up_":
                #pop() once to get up to the current level (equivalent to making a subcolumn at the current level)
                self.typeAddress.pop()
                #Go up as many times as there are consecutive "_up_" in typeList, 
                #   popping the address each time, 
                #   and increasing the typeList index until getNextCommandOrType() returns a type
                command = typeOrCommand
                while command == "_up_":
                    self.typeAddress.pop()
                    command = self.getNextCommandOrType() 

                #Get the Type that is after the 1 or more "_up_" commands
                if command == "_end_":
                    self.writeReport()
                    raise NotImplementedError("Implement writing the report and getting ready for processing another folder of photos")
                else:
                    typeAfterCommands = command

                #Get the current dict in the allData nested dict
                parentOrGrandparent = self.getCurrentDict_InAllData()

                #Create the new section of the data JSON
                parentOrGrandparent['subcolumns'][typeAfterCommands] = {"data": parentOrGrandparent['data'].copy(), "subcolumns":{}}

                #Update the typeAddress to point to the new part of the allData nested dict
                self.typeAddress.append(typeAfterCommands)
            case "_end_":
                raise NotImplementedError("_end_ should only be after 1 or more _up_s, so this should not be hit", self.typesList)
            case _:
                #Update the typeAddress to point to the parent, since the new Type will be a subcolumn of the parent
                self.typeAddress.pop()
                parent = self.getCurrentDict_InAllData()

                #Create the new section of the allData nested dict
                parent['subcolumns'][typeOrCommand] = {"data": parent['data'].copy(), "subcolumns":{}}

                #Update the typeAddress to point to the new part of the allData nested dict
                self.typeAddress.append(typeOrCommand)

        #Tell the UI to update the "Is there a ____?" area
        self.looking4Changed.emit(self.typeAddress[-1])

        #Flash the Typechange Icon on screen so the user knows that we are changing types
        self.flashIcon.emit("typechange")

        self.getNextPhoto()

    def getNextPhoto(self):
        #Move through the pics until hitting the next one that is relevant for the current Type
        #   i.e. If the current Type is "Camel", it skips all photos where "Domestic Animal" was answered no
        #   This works because the data for "Domestic Animal" was copied into "Camel" and is simply being modified.
        current = self.getCurrentDict_InAllData()
        self.picIndex = self.picIndex + 1
        try:
            while current['data'][self.picIndex] == 0:
                self.picIndex = self.picIndex + 1
        except IndexError as error:
            self.moveToNextType()
            
        #Fetch the picture URL and pass it back
        nextPicURL = self.pictureURLs[self.picIndex]
        return nextPicURL
    
    def getLastPhoto(self):
        if self.picIndex == 0:
            #Going back to the last Type is going to require a special handling case
            print("Have not implemented going back to the last Type yet.")
        else:
            self.picIndex = self.picIndex - 1

            return self.pictureURLs[self.picIndex]
    

    #Accept a folder URL, return the URL of the first picture in the list of pics in the folder.
    @Slot(str, result=str)
    def setFolder(self, folderURL):
        print("@Slot: folder URL: " + folderURL)

        #Fix this:  file:///Users/test/Pictures --> /Users/test/Pictures
        folderURLFixed = folderURL[7:]
        
        self.picIndex = -1

        #Get all files in the directory
        self.pictureURLs = natsorted(os.listdir(folderURLFixed))
        #Add the rest of the filepath to them
        self.pictureURLs = [folderURLFixed + '/' + file for file in self.pictureURLs if file.endswith(('.jpeg', '.JPEG', '.jpg', '.JPG'))]

        #Set the "Any Trigger" data list to be a number of 1s equal to the number of pictures.
        #   In a data list, a 1 that has not been accessed yet means that it needs to be checked.
        #   This is because the data list is passed down the allData dict tree from parent to children, to keep track of which pictures do not need to be checked for a Type
        #   Because if there is no "Domestic Animal" trigger, then there is no point asking if there is a "Donkey" trigger
        self.allData["Any Trigger"]["data"] = [1] * len(self.pictureURLs)

        #Set the UI to "Is there: Any Trigger?"
        self.looking4Changed.emit(self.typeAddress[-1])
        self.pictureChanged.emit('0' + "/" + str(len(self.pictureURLs)))

        #TESTING
        fileData = []
        self.getFileData(self.pictureURLs, fileData)
        #TESTING

        return self.getNextPhoto()
    
    @Slot(str, result=str)
    def choiceMade(self, choice):
        #Make sure the list of pictures has been initialized.
        if not self.pictureURLs:
            raise ValueError("pictureURLs List has not been initialized.", self.pictureURLs)

        #Update or roll back any data, then get the url for the picture that should be shown.        
        picToShow = "I'm A File URL"
        match choice.lower():
            case "yes":
                self.updateCurrentData(1)
                picToShow = self.getNextPhoto()
                self.flashIcon.emit("yes")
            case "no":
                self.updateCurrentData(0)
                picToShow = self.getNextPhoto()
                self.flashIcon.emit("no")
            case "back":
                self.updateCurrentData(1) #This is being set because it essentially sets the data point to "not filled in". See getNextPhoto() for explanation.
                picToShow = self.getLastPhoto()
                self.flashIcon.emit("back")
            case _:
                raise ValueError("user choice passed in is not valid. Should be \'yes\',\'no\', or \'back\' (case insensitive)" , choice)

        self.pictureChanged.emit(str(self.picIndex+1) + "/" + str(len(self.pictureURLs)))

        return picToShow
    
    @Slot(str)
    def recordNote(self, note):
        print(note)
        self.notes[self.picIndex] = note

    @Slot(result=str)
    def getNote(self):
        return self.notes.get(self.picIndex, "")
    