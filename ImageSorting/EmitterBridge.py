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
    
    otherTest = "wut"

    updateCategoryTracker = Signal(str)
    hideCategoryTracker = Signal()
    updatePhoto = Signal(str)
    updatePhotoCounter = Signal(str)
    hidePhotoCounter = Signal()
    flashIcon = Signal(str)
    showFolderSelectionArea = Signal()
    hideFolderSelectionArea = Signal()
    showNextCategoryExplanation = Signal(str)
    hideNextCategoryExplanation = Signal()
    showExplanation = Signal(str)
    hideExplanation = Signal()
    showPrintArea = Signal()

    def __init__(self):
        QObject.__init__(self)

    def wtf(self):
        self.updatePhoto.emit("test")
