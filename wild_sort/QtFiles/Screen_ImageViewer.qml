import QtQuick

Image {
    id: head
    width: page.width
    height:parent.height
    fillMode: Image.PreserveAspectFit
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    visible: false

    ShowerHider {
        code: "screen_imageviewer"
    }

    Focuser {
        id: photoFocuser
        code: "screen_imageviewer"
    }

    Setter{
        code: "photo"
        property alias prop: head.source
    }

    Keys.onPressed: (event)=> { 
        console.log("Key pressed from Screen_ImageViewer: " + event.key)

        event.accepted = true //Prevent key event from being handled again at base

        if (event.key == Qt.Key_L ){
            slotBridge.choiceMade("yes") 
        }
        if (event.key == Qt.Key_Semicolon){
            slotBridge.choiceMade("no")
        } 
        if (event.key == Qt.Key_Apostrophe){
            slotBridge.previousPhoto() 
        } 

        if (event.key == Qt.Key_Return || event.key == Qt.Key_Enter){
            if (!notesPopup.opened){
                //Fill out the category checkboxes on the Notes Popup
                var categoryData = slotBridge.getDataForPhoto()
                categoryCheckboxHolder.fillCategoryCheckboxes(categoryData)
                
                //Open the Notes Popup and fill in the text
                notesPopup.open()
                notes.text = slotBridge.getNote()

                //Handle focusing into the text field, and prepping for focusing back to the last item after Notes Popup is closed.
                notes.lastFocus = window.activeFocusItem
                notes.forceActiveFocus()
            }
        }
    }
}