import os
from PySide6.QtCore import QObject, Slot
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine, QmlElement
from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtCore import QObject, Signal, Property


# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "com.isort.emitterbridge"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class EmitterBridge(QObject):

    #Reuseables
    showElement = Signal(str)
    hideElement = Signal(str)
    focusElement = Signal(str)

    #Setters
    updateCategoryTracker = Signal(str)
    updatePhoto = Signal(str)
    updatePhotoCounter = Signal(str)
    showNextCategoryExplanation = Signal(str)
    fillCamAndLocForm = Signal(str, str)

    #Necessary?
    hideCategoryTracker = Signal()
    hidePhotoCounter = Signal()
    hideNextCategoryExplanation = Signal()

    #Icon
    flashIcon = Signal(str)

    #TO IMPLEMENT
    setCategoriesTutorial = Signal(str)
    createCategoryCheckboxes = Signal(list)

    def __init__(self):
        QObject.__init__(self)

    def wtf(self):
        self.updatePhoto.emit("test")
