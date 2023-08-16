import EmitterBridge as emitterBridge

emitter = emitterBridge.EmitterBridge()

def setPhoto_InUI(photoURL):
    emitter.updatePhoto.emit(photoURL)

def setPhotoCounter_InUI():
    photoCounter = str(self.photoIndex) + '/' + str(self.dataManager.countPicsInCategory(self.categoryIndex))
    emitter.updatePhotoCounter.emit(photoCounter)


def setCategory_InUI():
    #TODO: Add a delay of 0.2 seconds
    emitter.updateCategory.emit(self.dataManager.dataList[self.categoryIndex]['title'])
    
def clearPhotoIn_UI():
    emitter.updatePhoto.emit('')
    emitter.updatePhotoCounter.emit('-/-')

def show_NextCategoryWillBe_InUI():
    #TODO: Add a delay of 0.2 seconds
    emitter.showNextCategoryExplanation.emit("Next Category will be: " + self.dataManager.dataList[self.categoryIndex + 1]['title'])
    emitter.updatePhoto.emit('AppImages/restart-arrow.png')
    emitter.updatePhotoCounter.emit('-/' + str(self.dataManager.countPicsInCategory(self.categoryIndex + 1)))

def hide_NextCategoryWillBe_UI():
    emitter.hideNextCategoryExplanation.emit()

def show_AreYouReadyToPrintReportButton_InUI():
    #TODO: Add a delay of 0.2 seconds
    #TODO IMPLEMENT button and showing button.
    emitter.updatePhoto.emit('')
    emitter.updatePhotoCounter.emit('')