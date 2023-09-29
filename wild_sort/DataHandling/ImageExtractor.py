import os

from natsort import natsorted


def getImages(folderURL: str) -> list[str]:
    """Gets the URLs of all 'jpeg' images in the folder and subfolders, natsorted."""
    cleaned = _cleanURL(folderURL)

    print(f"cleaned: {cleaned}")

    #Get all files in the directory
    photoURLs = _recursiveGetFiles(cleaned)
    #Cut out any that aren't jpeg
    photoURLs = [file for file in photoURLs if file.endswith(('.jpeg', '.JPEG', '.jpg', '.JPG'))]
    #Sort 
    photoURLs = natsorted(photoURLs)


    print(f"sorted: {photoURLs}")

    return photoURLs
    

def _recursiveGetFiles(folderURL):
    #os.listdir(folderURL)
    allFiles = []
    for folderPath, subfolders, files in os.walk(folderURL):

        print(f"folderURL: {folderURL}")
        print(f"folderPath: {folderPath}")
        #Make sure it is the full URL, not just the filename
        allFiles.extend([(folderPath + '/' + file) for file in files]) 

    return allFiles

def _cleanURL(dirty: str) -> str:
    """This returns a useable URL based on the operating system. It should pass the associated test in /Testing/Test_ImageExtractor"""
    better = dirty.split(':',1)[1]
    
    if ':' in better: #This is true if operating system is Windows
        return better[3:]
    else:
        return better[2:]

