from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import datetime
import os
import shutil

import exifread

import DataHandling.DataManager as DataManager


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

    def getRows(self):
        """Flips data sideways, from columns to rows. B/c you can't print columns to a spreadsheet."""
        return zip(*self.columns)


def buildReports_Human(dataList:list[DataManager.Category], photoURLs:list[str], notes:list[str]):
    """
Converts all relevant data into a human-readable and visualization-friendly report. 
\nBacks up any existing 'cameraTrapData.csv' file in the folder of photos.
\nPrints to a spreadsheet called 'cameraTrapData.csv' in the folder of photos.
\nTODO: Adds all rows to an 'ALL_cameraTrapData_DO_NOT_EDIT.csv' file in the working directory.
    """
    addCategoriesToPhotoName(DataManager.dataList)

    report = _collateReport(dataList, photoURLs, notes)

    ##Handle StandAlone report
    target_StandAlone = folderOfPhotos + '/cameraTrapData.csv'

    if os.path.exists(target_StandAlone):
        _convertToHiddenBackup(fileURL=target_StandAlone)
        
    _printReport(report.headers, data=report.getRows(), filename=target_StandAlone)

    ##Handle AllData report
    target_AllData = './ALL_cameraTrapData_DO_NOT_EDIT.csv'

    if os.path.exists(target_AllData):
        _convertToHiddenBackup(fileURL=target_AllData)
        _appendReport(data=report.getRows(), filename=target_AllData)
    else:
        _printReport(report.headers, data=report.getRows(), filename=target_AllData)



def buildReport_AI():
    """Collects all relevant data for the human report and prints it to a file called..."""
    raise NotImplementedError("Not written yet")

def _collateReport(dataList:list[DataManager.Category], photoURLs:list[str], notes:list[str]) -> ReportParts:
    
    fullReport = ReportParts([],[])
    #Columns 1 & 2
    fullReport.add( 
        getLocAndCamera(location, camera, len(photoURLs))
    )

    #This fills the columns 3-5 of the report: 
    #   'Link To File', 'Date', 'Time'
    fullReport.add( 
        _getAllFiledata(photoURLs)
    )

    #Get Notes
    fullReport.add( 
        _getNoteColumn(photoURLs, notes)
    )

    #Add the Data Columns (Any Trigger, Human, Domestic, Donkey, Wild Animal, etc)
    fullReport.add( 
        _getDataColumns(dataList)
    )

    return (fullReport)



def _convertToHiddenBackup(fileURL):
    """Example: Renames '/folder/file.csv' -> '/folder/.file_backup.csv'"""
    head, tail = os.path.split(fileURL)
    fileName, fileType = tail.split('.')
    backupURL = head + '/.' + fileName + '_backup.' + fileType
    shutil.copyfile(src=fileURL, dst=backupURL)

def _getDataColumns(dataList: list[DataManager.Category]):
    headers=[]
    columns=[]
    for category in dataList:
        headers.append(category.title)
        columns.append(_cleanDataColumn(category.data))

    return ReportParts(headers, columns)

def _cleanDataColumn(dataColumn):
    '''Converts the 'skip's used by SortLogic.py to skip pictures, into 0s, so that the report is pretty'''
    cleaned = [0 if (data == 'skip') else data for data in dataColumn]

    if 0 < len([data for data in cleaned if (data != 1 and data != 0)]):
        raise ValueError(cleaned, 'dataColumn should have only 1s and 0s')

    return cleaned


def _printReport(headers, data, filename):
    with open(filename, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the columns headers
        writer.writerow(headers)

        # write multiple rows
        writer.writerows(data)


def _appendReport(data, filename):
    with open(filename, 'a', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        #TODO: Check if the columns match

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
def _getAllFiledata(photoURLs):
    fileLink_Column = []
    dateTaken_Column = []
    timeTaken_Column = []

    for url in photoURLs:
        fileData = _getFileData(url)
        
        dateTaken_Column.append(fileData[0])
        timeTaken_Column.append(fileData[1])

        justTheFolderName = folderOfPhotos.split('/')[-1]
        splitURL = url.split(justTheFolderName, 1)

        if len(splitURL) == 1:
            raise ValueError(url, folderOfPhotos, 'folderOfPhotos should be found in the middle of the url')
        else:
            shortenedURL = splitURL[1]
        fileLink_Column.append(f"=HYPERLINK(\"\"{url}\"\";\"\"{shortenedURL}\"\")")

    return ReportParts(
        headers=['Link To File', 'Date', 'Time'],
        columns=[
            fileLink_Column, 
            dateTaken_Column, 
            timeTaken_Column
        ]
    )


def _getFileData(fileURL):
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
    

def _getNoteColumn(photoURLs, notes:dict):
    notesColumn = [''] * len(photoURLs)

    tutorialNote = notes.get(-1)
    del notes[-1] #Remove -1 key if it exists

    for key in notes:
        notesColumn[key] = notes[key]

    notes[-1] = tutorialNote

    return ReportParts(
        headers=['Notes'],
        columns=[notesColumn]
    )


##################----------------------------
###Adding categories to photo names
##################----------------------------

def addCategoriesToPhotoName(dataList: list[DataManager.Category]):
    for category in dataList:
        for index, photoURL in enumerate(DataManager.photoURLs):
            if category.data[index] == 1:
                head, tail = os.path.split(photoURL)
                fileName, fileType = tail.split('.')
                newName = head + '/' + fileName + '_' + category.title + '.' + fileType
                os.rename(photoURL, newName)
                DataManager.photoURLs[index] = newName

    for index, photoURL in enumerate(DataManager.photoURLs):
        note = DataManager.notes.get(index, None)
        if note != None:
            head, tail = os.path.split(photoURL)
            fileName, fileType = tail.split('.')
            newName = head + '/' + fileName + '_' + note + '.' + fileType
            os.rename(photoURL, newName)
            DataManager.photoURLs[index] = newName