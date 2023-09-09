import os

from natsort import natsorted


def getImages(folderURL: str) -> list[str]:
    """Gets the URLs of all 'jpeg' images in the folder and subfolders, natsorted."""
    cleaned = _cleanURL(folderURL)

    #Get all files in the directory
    photoURLs = __recursiveGetFiles(folderURL)
    #Cut out any that aren't jpeg
    photoURLs = [file for file in photoURLs if file.endswith(('.jpeg', '.JPEG', '.jpg', '.JPG'))]
    #Sort 
    photoURLs = natsorted(photoURLs)

    return photoURLs
    

def __recursiveGetFiles(folderURL):
    #os.listdir(folderURL)
    allFiles = []
    for folderPath, subfolders, files in os.walk(folderURL):
        #Make sure it is the full URL, not just the filename
        allFiles.extend([(folderPath + '/' + file) for file in files]) 

    return allFiles

def _cleanURL(dirty: str) -> str:
    #TODO: This should return a useable URL based on the operating system. It should pass the associated test in /Testing/Test_ImageExtractor
    return dirty

