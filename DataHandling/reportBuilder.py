import csv
from dataclasses import dataclass
from datetime import datetime

import exifread


location = ''
camera = ''

@dataclass
class ReportParts():
    headers: []
    columns: [[]]

    def add(self, newParts): #Why does declaring type, ie: "newParts: reportParts" not work?
        if ReportParts != type(newParts):
             raise TypeError
        self.headers.extend(newParts.headers)
        self.columns.extend(newParts.columns)


def writeReport_Human(dataList, photoURLs, notes):
    """Collects all relevant data for the human report and prints it to spreadsheet called transactData.csv"""

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
        getDataColumns(dataList)
    )


    #Flip data sideways before printing the report. 
    #   B/c you can't print columns to a spreadsheet
    rows = zip(*fullReport.columns)
    

    printReport(fullReport.headers, rows, 'transactData.csv')
    #TODO: also print to a 'transactData_AllData_doNOTedit' and a hidden one (.transactData_AllData)


def getDataColumns(dataList):
    headers=[]
    columns=[]
    for datachunk in dataList:
        headers.append(datachunk['category'])
        columns.append(cleanDataColumn(datachunk['data']))

    return ReportParts(headers, columns)

def cleanDataColumn(dataColumn):
    '''Converts the -1s used by SortLogic.py to skip pictures, into 0s, so that the report is pretty'''
    cleaned = [0 if (data == -1) else data for data in dataColumn]

    if 0 < len([data for data in cleaned if (data != 1 and data != 0)]):
        raise ValueError(cleaned, 'dataColumn should have only 1s and 0s')

    return cleaned

def writeReport_AI():
    """Collects all relevant data for the human report and prints it to the spreadsheet called aiData.csv"""
    raise NotImplementedError("Not written yet")



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
