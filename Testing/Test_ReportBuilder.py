import random
import unittest

import DataHandling.ReportBuilder as reportBuilder
import DataHandling.DataManager as data

# The test based on unittest module
class Test_WriteReport(unittest.TestCase):
    photoURLs = [
        './Testing/testingMaterial/dirt.JPG',
        './Testing/testingMaterial/elephant.jpeg',
        './Testing/testingMaterial/feet.JPG',
        './Testing/testingMaterial/hyena.jpeg'
        ]
    
    
    def test_getLocationAndCamera(self):
        #Expected Result
        expectedColumns = [
        ['lapusse']*4,
        ['B1']*4
        ]

        #Run Function
        result = reportBuilder.getLocAndCamera('lapusse', 'B1', 4)

        #Assertions
        self.assertEqual(expectedColumns, result.columns, 'loc & camera data wrong')
        

    def test_getFiledata(self):
        #Expected Result
        expectedURLColumn = [
            '=HYPERLINK(\"\"./Testing/testingMaterial/dirt.JPG\"\";\"\"/dirt.JPG\"\")',
            '=HYPERLINK(\"\"./Testing/testingMaterial/elephant.jpeg\"\";\"\"/elephant.jpeg\"\")',
            '=HYPERLINK(\"\"./Testing/testingMaterial/feet.JPG\"\";\"\"/feet.JPG\"\")',
            '=HYPERLINK(\"\"./Testing/testingMaterial/hyena.jpeg\"\";\"\"/hyena.jpeg\"\")'
        ]
        expectedColumns = ([
            expectedURLColumn,
            ['2021/08/12', '2004/06/03', '2021/08/06', ''],
            ['07:09:48', '16:53:30', '11:56:39', '']
        ])

        #Run Function
        reportBuilder.folderOfPhotos = './Testing/testingMaterial'
        result = reportBuilder._getAllFiledata(self.photoURLs)
        
        #Assertions
        self.assertEqual(expectedColumns, result.columns, 'filedata columns wrong')


    def test_getNotes(self):
        #Expected Result
        expectedColumns = [[
            '',
            'elephant',
            '',
            'hyena'
        ]]

        #Run Function
        data.setNote(1, 'elephant')
        data.setNote(3, 'hyena')
        result = reportBuilder._getNoteColumn(self.photoURLs, data.notes)

        #Assertions
        self.assertEqual(expectedColumns, result.columns, 'note column wrong')

        
    def test_cleanDataColumn(self):
        testDataColumn = [0,1,'skip',0,1,'skip']
        cleaned = reportBuilder._cleanDataColumn(testDataColumn)
        self.assertEqual(cleaned, [0,1,0,0,1,0], 'cleaning column did not work as expected')

        self.assertRaises(ValueError,reportBuilder._cleanDataColumn,[0,1,'skip',-1])
        self.assertRaises(ValueError,reportBuilder._cleanDataColumn,[0,1,'skip',-2])
        self.assertRaises(ValueError,reportBuilder._cleanDataColumn,[0,1,'skip',None])


    def test_getData(self):
        #Expected Result
        expectedHeaders = ['Any Trigger', 'Human Elements', 'People', 'Motorbikes', 'Cars', 'Domestic Animals', 'Shoats', 'Camels', 'Donkeys', 'Cattle', 'Domestic Dogs', 'Wild Animals']
        expectedData = []

        for category in data.dataList:
            randomData = random.sample(['skip',0,1],counts=[4,4,4],k=4)
            category.data = randomData
            expectedData.append(reportBuilder._cleanDataColumn(randomData)) #cleanDataColumn is tested elsewhere

        result = reportBuilder._getDataColumns(data.dataList)

        #Assertions
        self.assertEqual(expectedHeaders, result.headers, 'headers wrong')
        self.assertEqual(expectedData, result.columns, 'data wrong')

if __name__ == '__main__':
    unittest.main()

 
# tests = Test_WriteReport()
# tests.test_getLocationAndCamera()
# tests.test_getFiledata()
# tests.test_getNotes()
# tests.test_cleanDataColumn()
# tests.test_getData()

