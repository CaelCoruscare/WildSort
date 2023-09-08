import random
import unittest

import DataHandling.ImageExtractor as extractor

class Test_ImageExtractor(unittest.TestCase):

    def test_cleanURL(self):
        testURLS = [
            'file:///C://Users/Toby/Photos',
            'file:///Users/Cael/Photos'
        ]

        expectedResults = [
            'C://Users/Toby/Photos',
            '/Users/Toby/Photos'
        ]

        resultURLs = []

        #Run Function
        resultURLs.extend([
            extractor._cleanURL(testURLS[0]),
            extractor._cleanURL(testURLS[1])

        ])

        #Assertions
        self.assertEqual(expectedResults[0], resultURLs[0], 'Windows file cleaning failed')
        self.assertEqual(expectedResults[1], resultURLs[1], 'Unix file cleaning failed')

if __name__ == '__main__':
    unittest.main()