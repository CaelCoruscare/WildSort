import unittest

import DataHandling.ReportBuilder as reportBuilder

# The test based on unittest module
class TestWriteReport(unittest.TestCase):
    def test_getLocationAndCamera(self):
        testHeaders = ['Corridor', 'Camera', 'Link To File', 'Date', 'Time', 'Note']
        testData = [
            ['lapusse']*4,
            ['B1']*4
            ]
        reportBuilder.fillLocationAndCameraData('lapusse', 'B1', 4)
        self.assertEqual(testHeaders, reportBuilder.reportHeaders_Human, 'headers wrong')
        self.assertEqual(testData, reportBuilder.reportData_Human, 'data wrong')
        
    def test_getFileData(self):
        photoURLs = [
            './testingMaterial/dirt.JPG',
            './testingMaterial/elephant.jpeg',
            './testingMaterial/feet.JPG',
            './testingMaterial/hyena.jpeg'
            ]

        reportBuilder.getFileData(photoURLs)

        
        #self.assertEqual(reportHeaders_Human, , "incorrect area")
        #self.assertEqual(reportData_Human, , "incorrect area")
 
# run the test
if __name__ == '__main__':
    unittest.main()