from ImageSorting.EmitterBridge import EmitterBridge
emitter = EmitterBridge()
           

def setPhoto(photoURL):
    """Sets the photo source. Can also set the Photo Counter text obj."""
    if photoURL == None:
        photoURL = ''
    emitter.updatePhoto.emit(photoURL)

def setPhotoCounter(photoCounter):
    emitter.updatePhotoCounter.emit(photoCounter)

def setCategory(title):
    if title == None:
        emitter.hideCategoryTracker.emit()
    else:
        emitter.updateCategoryTracker.emit(title)

def show_NextCategoryWillBe(category):
    if category == None:
        emitter.hideNextCategoryExplanation.emit()
    else:   
        emitter.showNextCategoryExplanation.emit(category)
        emitter.updatePhoto.emit('AppImages/restart-arrow.png')

def hide_NextCategoryWillBe():
    emitter.hideNextCategoryExplanation.emit()


def flashIcon(userAnswer):
    match userAnswer:
        case 1:
            emitter.flashIcon.emit('yes')
        case 0:
            emitter.flashIcon.emit('no')
        case _:
            emitter.flashIcon.emit(userAnswer)



def show_KeysTutorial():
    emitter.showKeysTutorial.emit()

def hide_KeysTutorial():
    emitter.hideKeysTutorial.emit()

def show_AreYouReadyToPrintReport():
    #TODO IMPLEMENT button and showing button.
    emitter.updatePhoto.emit('')
    emitter.updatePhotoCounter.emit('')
    emitter.showPrintArea.emit()

def showCamAndLocForm(camera, location):
    emitter.showCamAndLocForm.emit(camera, location)


##---This is cool so I'm leaving it as a comment to reference for later.---
# def flashIcon(answer):
#     """Takes int (0,1) or string('yes', 'no', 'back')"""
#     _flashIcon_Map[type(answer)](answer)


# def _flashIcon_Int(userAnswer: int):
#     match userAnswer:
#         case 1:
#             emitter.flashIcon.emit('yes')
#         case 0:
#             emitter.flashIcon.emit('no')
#         case _:
#             pass

# def _flashIcon_Str(code: str):
#     match code:
#         case 'yes':
#             emitter.flashIcon.emit('yes')
#         case 'no':
#             emitter.flashIcon.emit('no')
#         case 'back':
#             emitter.flashIcon.emit('back')
#         case _:
#             pass

# _flashIcon_Map = {
#             int : _flashIcon_Int,
#             str : _flashIcon_Str
# }