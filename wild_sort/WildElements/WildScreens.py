from __future__ import annotations

from ast import Tuple
import os

import ImageSorting.CallsToUI as ui
from DataHandling import DataManager
from DataHandling.DataManager import index, notes
from DataHandling import ReportBuilder
from ImageSorting import SortLogic

from WildElements.WildElement import WildElement


class WildScreen(WildElement):
    _previousScreen: WildScreen
    _nextScreen: WildScreen

    def __init__(self, code: str, previousScreen: WildScreen):
        super().__init__(code)

        self._previousScreen = previousScreen
        if previousScreen != None:
            previousScreen._nextScreen = self

    def nextScreen(self) -> WildScreen:
        self.hide()
        self._nextScreen.show()

        return self._nextScreen
    
    def show(self):
        self.focus()
        return super().show()
    
    def previousScreen(self) -> WildScreen:
        self.hide()
        self._previousScreen.show()
        ui.flashIcon('back')

        return self._previousScreen
    
    def sort(self, yesOrNo: int):
        """By default does nothing. Must be implemented, since most screens do not allow opening Notes."""
        return

    def openNotes(self):
        """By default does nothing. Must be implemented, since most screens do not allow opening Notes."""
        return
    
    def saveNote(self, note):
        """By default does nothing. Must be implemented, since most screens do not allow opening Notes."""
        return
    pass


class ChooseFolder(WildScreen):
    def previousScreen(self) -> WildScreen:
        return self #Ignore going back on this screen
    pass


class CameraAndLocation(WildScreen):
    _cameraField = WildElement(code='field_camera')
    _locationField = WildElement(code='field_location')

    def show(self):
        super().show()

        cameraText, locationText = self._getDefaultValues()

        self._cameraField.set(cameraText)
        self._locationField.set(locationText)

    def focus(self):
        self._locationField.focus()

    def hide(self): 
        super().hide()
        #Make sure indexes are set proper
        index.category = -1
        index.photo = -1

    def _getDefaultValues(self)-> Tuple[str, str]:
        camera = os.path.basename(ReportBuilder.folderOfPhotos)
        location = ReportBuilder.location

        return (camera, location)
    pass


class TutorialKeys(WildScreen):
    _tutorialNote = 'You can put your notes here when a picture is open. This can be useful for an unusual animal, or marking rare cases of vandalism, or anything else worth jotting down.'

    def openNotes(self):
        """Uses a special Tutorial Note to avoid messing with the report builder"""
        ui.openNotes(note=self._tutorialNote)

    def saveNote(self, note:str):
        """Uses a special Tutorial Note to avoid messing with the report builder"""
        self._tutorialNote = note
        
    
    pass


class TutorialWhatClick(WildScreen):
    def hide(self):
        super().hide()
        #Skip over tutorials when you select the next folder.
        camAndLoc = self._previousScreen._previousScreen
        camAndLoc._nextScreen = self._nextScreen
    pass


class NextCategory(WildScreen):
    _nextCategoryText = WildElement('text_nextcategory')
    _photoCounter = WildElement('text_photocounter')

    def show(self):
        super().show()   
        nextCategory = DataManager.getCategory(index.category + 1)
        self._nextCategoryText.set('Next category: <b>' + nextCategory.title + '</b>')
        self._nextCategoryText.show()
        self._photoCounter.set( '-/' + str(nextCategory.countPhotos()) )
        self._photoCounter.show()

    def nextScreen(self) -> WildScreen:
        index.category += 1
        index.photo = -1
        return super().nextScreen()

    def previousScreen(self)->WildScreen:
        if index.category == -1:
            return self #Can't go back from the first NextCategory screen.
        else:
            index.photo -= 1 #index.photo > index.photoMax means "on NextCategory screen"
            return super().previousScreen()
    pass


class ImageViewer(WildScreen):
    _categoryText = WildElement('text_categoryis')
    _photoCounter = WildElement('text_photocounter')

    def show(self):
        super().show()
        cat = DataManager.getCategory(index.category)
        self._categoryText.set(cat.title)
        self._categoryText.show()
        self._photoCounter.set( str(index.photo+1) + '/' + str(cat.countPhotos()) )

    def hide(self):
        super().hide()
        self._categoryText.hide()
        self._photoCounter.hide()

    def previousScreen(self) -> WildScreen:
        index.photo = index.photoMax() + 1 #index.photo > index.photoMax means "on NextCategory screen"
        index.category -= 1
        return super().previousScreen()
    
    def nextScreen(self) -> WildScreen:
        if index.category == len(DataManager.dataList) - 1:
            return super().nextScreen() #Go to PrintReport Screen.
        else:
            DataManager.getCategory(index.category +1).initializeData()
            #Go for another loop through a different Category       
            self.hide()
            self._previousScreen.show()

            return self._previousScreen
    pass


class PrintReport(WildScreen):
    def focus(self):
        return super().focus()
    pass

class ScreenManager():
    """Initializes a looping list of Screens, and keeps track of the current Screen."""
    currentScreen: WildScreen

    def __init__(self):
        cf = ChooseFolder('screen_choosefolder', None)
        cl = CameraAndLocation('screen_cameralocation', previousScreen=cf)
        tk = TutorialKeys('screen_tutorial_keys', previousScreen=cl)
        tw = TutorialWhatClick('screen_tutorial_whatclick', previousScreen=tk)
        nc = NextCategory('screen_nextcategory', previousScreen=tw)
        im = ImageViewer('screen_imageviewer', previousScreen=nc)
        pr = PrintReport('screen_printreport', previousScreen=im)
        pr._nextScreen = cf #Loop back to front

        #Hitting back on a NextCategory Screen should loop forward to ImageViewer
        nc._previousScreen = im

        #This keeps the screens referenced so they aren't cleaned up. Not sure if necessary.
        self._screens = [cf,cl,tk,tw,nc,im,pr] 

        #This will be used to interact from outside the module
        self.currentScreen = cf
        self.currentScreen.show()

    def next(self):
        self.currentScreen = self.currentScreen.nextScreen()

    def back(self):
        self.currentScreen = self.currentScreen.previousScreen()

screenManager = ScreenManager()