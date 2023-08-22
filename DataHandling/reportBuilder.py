import csv
from datetime import datetime

import unittest

import exifread



#This will hold all the report headers for the final human report
reportHeaders_Human = ['Corridor', 'Camera', 'Link To File', 'Date', 'Time', 'Note']#Data columns will be appended

#This is a list of all the columns in the final human report. File columns, notes, data columns, etc. Everything.
reportData_Human = []
#

def writeReport_Human(dataList, photoURLs, notes):
    """Collects all relevant data for the human report and prints it to spreadsheet called transactData.csv"""

    #Columns 1 & 2 should have been filled after the folder was opened, using:
    #   fillLocationAndCameraData(location, camera, numPhotos)


    #This fills the columns 3-5 of the report: 
    #   'Link To File', 'Date', 'Time'
    getFileData(photoURLs)

    #Get Notes
    reportData_Human[5] = getNotesData(photoURLs, notes)

    #Add the Data Columns (Any Trigger, Human, Domestic, Donkey, Wild Animal, etc)
    for datachunk in dataList:
        reportHeaders_Human.append(datachunk['category'])
        reportData_Human.append(datachunk['data'])
    
    #Flip data sideways before printing the report. 
    #   B/c you can't print columns to a spreadsheet
    dataRotated = zip(*reversed(reportData_Human))
    
    

    printReport(reportHeaders_Human, dataRotated, 'transactData.csv')
    #TODO: also print to a 'transactData_AllData_doNOTedit' and a hidden one (.transactData_AllData)


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
def fillLocationAndCameraData(location, camera, numPhotos):
    reportData_Human.append([location] * numPhotos)
    reportData_Human.append([camera] * numPhotos)

#This fills the columns 3-5 of the report: 
#   'Link To File', 'Date', 'Time'
def getFileData(photoURLs):
    for url in photoURLs:
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
        reportData_Human.append(
            linkToFile, 
            dateTaken,
            timeTaken
        )

def getNotesData(photoURLs, notes):
    notesColumn = [""] * len(photoURLs)

    del notes[-1]

    for key in notes:
        notesColumn[key] = notes[key]


##################----------------------------
###TESTING BELOW
##################----------------------------

# # The test based on unittest module
# class TestWriteReport(unittest.TestCase):
#     def runTest(self):
#         fillLocationAndCameraData("test location", "test camera name", 8)


#         testHeaders = []
#         testData = [[],[],[]]
#         self.assertEqual(reportHeaders_Human, , "incorrect area")
#         self.assertEqual(reportData_Human, , "incorrect area")
 
# # run the test
# unittest.main()