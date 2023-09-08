from enum import Enum
from ImageSorting.EmitterBridge import EmitterBridge
emitter = EmitterBridge()
           
class Screen(Enum):
    SCREEN_LOAD_FOLDER = 'screen_loadfolder'
    SCREEN_CAMERA_LOCATION = 'screen_cameralocation'
    TUTORIAL_KEYS = 'tutorial_keys'
    TUTORIAL_CATEGORIES = 'tutorial_categories'
    TUTORIAL_IMAGES = 'tutorial_images'
    SCREEN_PRINT_REPORT = 'screen_printreport'


def showScreen(screen: Screen):
    match screen:
            case Screen.SCREEN_CAMERA_LOCATION:
                emitter.showElement.emit(screen.value)
                emitter.focusElement.emit('field_location')

            case _:
                emitter.showElement.emit(screen.value)
                emitter.focusElement.emit(screen.value)
        

def hideScreen(screen: Screen):
    emitter.hideElement.emit(screen.value)


def flashIcon(userAnswer):
    match userAnswer:
        case 1:
            emitter.flashIcon.emit('yes')
        case 0:
            emitter.flashIcon.emit('no')
        case 'continue':
            pass
        case _:
            emitter.flashIcon.emit(userAnswer)

#Should really refactor these so the show/hide functionality is separated out.
def set_Photo(photoURL):
    """Sets the photo source. Can also set the Photo Counter text obj."""
    if photoURL == None:
        photoURL = ''
    emitter.updatePhoto.emit(photoURL)

def set_PhotoCounter(photoCounter):
    if photoCounter == None:
        photoCounter = ''
    emitter.updatePhotoCounter.emit(photoCounter)

def set_Category(title):
    if title == None:
        emitter.hideCategoryTracker.emit()
    else:
        emitter.updateCategoryTracker.emit(title)

def set_CamAndLocForm(camera, location):
    emitter.fillCamAndLocForm.emit(camera, location)

def set_NextCategoryWillBe(category):
    if category == None:
        emitter.hideElement.emit("screen_nextcategory")
    else:   
        emitter.showNextCategoryExplanation.emit(category)
        emitter.updatePhoto.emit('AppImages/restart-arrow.png')

def set_CategoriesScreen(text):
    """This should be called only once, at start-up of the app"""
    emitter.setCategoriesTutorial.emit(text)




def createCategoryCheckboxes():
    emitter.createCategoryCheckboxes.emit(['test 1', 'test 2', 'test 3'])














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