from enum import Enum
from ImageSorting.EmitterBridge import EmitterBridge
emitter = EmitterBridge()
           
class SimpleElement(Enum):
    DIALOG_LOAD_FOLDER = 1
    TUTORIAL_KEYS = 2
    TUTORIAL_CATEGORIES = 3
    TUTORIAL_IMAGES = 4
    DIALOG_PRINT_REPORT = 5


def showSimple(element: SimpleElement):
    match element:
            case SimpleElement.DIALOG_LOAD_FOLDER:
                __show_LoadFolder()
            case SimpleElement.TUTORIAL_KEYS:
                __show_KeysTutorial()
            case SimpleElement.DIALOG_PRINT_REPORT:
                __show_PrintReportArea()
            case _:
                raise ValueError(element, "Unexpected Element")
        
def hideSimple(element: SimpleElement):
    match element:
            case SimpleElement.DIALOG_LOAD_FOLDER:
                __hide_LoadFolder()
            case SimpleElement.TUTORIAL_KEYS:
                __hide_KeysTutorial()
            case SimpleElement.DIALOG_PRINT_REPORT:
                __hide_PrintReportArea()
            case _:
                raise ValueError(element, "Unexpected Element")


def set_Photo(photoURL):
    """Sets the photo source. Can also set the Photo Counter text obj."""
    if photoURL == None:
        photoURL = ''
    emitter.updatePhoto.emit(photoURL)
    #print(f'photo: {photoURL}')

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
    if camera == None:
        emitter.hideCamAndLocForm.emit()
    else:
        emitter.showCamAndLocForm.emit(camera, location)
    #This form hides itself upon the button being clicked

def set_NextCategoryWillBe(category):
    if category == None:
        emitter.hideNextCategoryExplanation.emit()
    else:   
        emitter.showNextCategoryExplanation.emit(category)
        emitter.updatePhoto.emit('AppImages/restart-arrow.png')

def set_CategoriesScreen(text):
    """This should be called only once, at start-up of the app"""
    emitter.setCategoriesTutorial.emit(text)

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

###Show() methods
def __show_KeysTutorial():
    emitter.showKeysTutorial.emit()

def __show_LoadFolder():
    emitter.showKeysTutorial.emit()

def __show_PrintReportArea():
    emitter.showPrintArea.emit()

###Hide() methods
def __hide_KeysTutorial():
    emitter.hideKeysTutorial.emit()

def __hide_PrintReportArea():
    emitter.showPrintArea.emit()

def __hide_LoadFolder():
    emitter.hide_loadFolder.emit()

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