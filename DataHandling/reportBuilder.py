from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
import os
from typing import Tuple

import exifread

import DataHandling.DataManager as data


location = ''
camera = ''
folderOfPhotos = 'this is the folder url where the photos were pulled from'

@dataclass
class ReportParts():
    headers: []
    columns: [[]]

    def add(self, newParts: ReportParts):
        self.headers.extend(newParts.headers)
        self.columns.extend(newParts.columns)


def buildReports_Human(dataList:list[data.Category], photoURLs:list[str], notes:list[str]):
    """
Converts all relevant data into a human-readable and visualization-friendly report. 
\nBacks up any existing 'cameraTrapData.csv' file in the folder of photos.
\nPrints to a spreadsheet called 'cameraTrapData.csv' in the folder of photos.
\nTODO: Adds all rows to an 'ALL_cameraTrapData_DO_NOT_EDIT.csv' file in the working directory.
    """
    report = __collateReport(dataList, photoURLs, notes)

    #Flip data sideways before printing the report. 
    #   B/c you can't print columns to a spreadsheet
    rows = zip(*report.columns)

    target = folderOfPhotos + '/cameraTrapData.csv'

    if os.path.exists(target):
        __convertToHiddenBackup(target)

    printReport(report.headers, rows, target)
    #TODO: also extend to a 'cameraTrapData_AllData_doNOTedit' in the application folder


def buildReport_AI():
    """Collects all relevant data for the human report and prints it to a file called..."""
    raise NotImplementedError("Not written yet")

def __collateReport(dataList:list[data.Category], photoURLs:list[str], notes:list[str]) -> ReportParts:
    
    fullReport = ReportParts([],[])
    #Columns 1 & 2
    fullReport.add( 
        getLocAndCamera(location, camera, len(photoURLs))
    )

    #This fills the columns 3-5 of the report: 
    #   'Link To File', 'Date', 'Time'
    fullReport.add( 
        getAllFiledata(photoURLs)
    )

    #Get Notes
    fullReport.add( 
        getNoteColumn(photoURLs, notes)
    )

    #Add the Data Columns (Any Trigger, Human, Domestic, Donkey, Wild Animal, etc)
    fullReport.add( 
        __getDataColumns(dataList)
    )

    return (fullReport)



def __convertToHiddenBackup(fileURL):
    """Example: Renames '/folder/file.csv' -> '/folder/.file_backup.csv'"""
    head, tail = os.path.split(fileURL)
    fileName, fileType = tail.split('.')
    backupURL = head + '.' + fileName + '_backup.' + fileType
    os.rename(fileURL, backupURL)

def __getDataColumns(dataList: list[data.Category]):
    headers=[]
    columns=[]
    for category in dataList:
        headers.append(category.title)
        columns.append(__cleanDataColumn(category.data))

    return ReportParts(headers, columns)

def __cleanDataColumn(dataColumn):
    '''Converts the 'skip's used by SortLogic.py to skip pictures, into 0s, so that the report is pretty'''
    cleaned = [0 if (data == 'skip') else data for data in dataColumn]

    if 0 < len([data for data in cleaned if (data != 1 and data != 0)]):
        raise ValueError(cleaned, 'dataColumn should have only 1s and 0s')

    return cleaned





def printReport(headers, data, filename):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the columns headers
        writer.writerow(headers)

        # write multiple rows
        writer.writerows(data)


#This fills columns 1 & 2 of the report:
#   'location', 'camera'
#   The point of these 2 columns is to distinguish data when reports are aggregated.
def getLocAndCamera(location, camera, numPhotos):
    return ReportParts(
        headers=['Corridor', 'Camera'],
        columns=[
            [location] * numPhotos,
            [camera] * numPhotos
        ]
    )

#This fills the columns 3-5 of the report: 
#   'Link To File', 'Date', 'Time'
def getAllFiledata(photoURLs):
    dateTaken_Column = []
    timeTaken_Column = []

    for url in photoURLs:
        fileData = getFileData(url)
        
        dateTaken_Column.append(fileData[0])
        timeTaken_Column.append(fileData[1])

    return ReportParts(
        headers=['Link To File', 'Date', 'Time'],
        columns=[
            photoURLs, 
            dateTaken_Column, 
            timeTaken_Column
        ]
    )


def getFileData(fileURL):
    with open(fileURL, 'rb') as fh:
        tags = exifread.process_file(fh)
        dateTimeTaken = tags.get("EXIF DateTimeOriginal")
        subsecTimeTaken = tags.get("EXIF SubsecTimeOriginal")

        if dateTimeTaken is None:
            return ('','')

        #2003:08:11 16:45:32
        datetime_obj = datetime.strptime(dateTimeTaken.printable, '%Y:%m:%d %H:%M:%S')

        if subsecTimeTaken is not None:
            datetime_obj = datetime_obj + subsecTimeTaken
        #Date Taken
        dateTaken = datetime_obj.date().strftime('%Y/%m/%d')

        #Time Taken
        timeTaken = datetime_obj.time().strftime('%H:%M:%S')

        return (dateTaken, timeTaken)
    

def getNoteColumn(photoURLs, notes):
    notesColumn = [''] * len(photoURLs)

    del notes[-1]

    for key in notes:
        notesColumn[key] = notes[key]

    return ReportParts(
        headers=['Notes'],
        columns=[notesColumn]
    )


##################----------------------------
###TESTING BELOW
##################----------------------------
