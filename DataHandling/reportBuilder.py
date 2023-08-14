import csv
from DataHandling.dataManager import dataManager

class reportBuilder():

    def writeReport_Human(self):
        """Collects all relevant data for the human report and prints it to spreadsheet called transactData.csv"""
        #Columns 1 & 2 should have been filled after the folder was opened.

        #This fills the columns 3-5 of the report: 
        #   'Link To File', 'Date', 'Time'
        dataManager.getFileData()

        #Add the Data Columns (Any Trigger, Human, Domestic, Donkey, Wild Animal, etc)
        for datachunk in dataManager.dataList:
            dataManager.reportHeaders_Human.append(datachunk['type'])
            dataManager.reportData_Human.append(datachunk['data'])
        
        #TODO: Flip data sideways before printing the report. 
            #B/c you can't print columns to a spreadsheet

        self.printReport(dataManager.reportHeaders_Human, dataManager.reportData_Human, 'transactData.csv')
        #TODO: also print to a 'transactData_AllData_doNOTedit' and a hidden one (.transactData_AllData)


    def writeReport_AI(self):
        """Collects all relevant data for the human report and prints it to the spreadsheet called aiData.csv"""
        raise NotImplementedError("Not written yet")



    def printReport(self, headers, data, filename):
        with open(filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)

            # write the columns headers
            writer.writerow(headers)

            # write multiple rows
            writer.writerows(data)


    #This fills columns 1 & 2 of the report:
    #   'location', 'camera'
    #   The point of these 2 columns is to distinguish data when reports are aggregated.
    def fillLocationAndCameraData(self, location, camera):
        self.reportData_Human.append([location] * len(self.photoURLs))
        self.reportData_Human.append([camera] * len(self.photoURLs))

    #This fills the columns 3-5 of the report: 
    #   'Link To File', 'Date', 'Time'
    def getFileData(self):
        for url in self.photoURLs:
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
            self.reportData_Human.append(
                linkToFile, 
                dateTaken,
                timeTaken
            )

    
