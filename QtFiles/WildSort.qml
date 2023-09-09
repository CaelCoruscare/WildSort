import QtCore
import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Dialogs
import Qt.labs.folderlistmodel 2.5
import QtQuick.Layouts

import com.isort.slotbridge 1.0
import com.isort.emitterbridge 1.0



Window {
    width: 1280
    height: 640
    visible: true
    title: qsTr("WildSort")
    id: window

    Connections{
        target: emitterBridge

        function onUpdateCategoryTracker(newCategory){
            textCategory.text = newCategory + "?"
            textCategory.visible = true
            textIsThereA.visible = true
        }
        function onHideCategoryTracker(newCategory){
            textCategory.visible = false
            textIsThereA.visible = false
        }
        function onUpdatePhoto(picURL){
            photo.source = picURL
        }
        function onUpdatePhotoCounter(counterText){
            textPhotoCounter.text = counterText
            textPhotoCounter.visible = true
            textPhotoNum.visible = true
        }
        function onHidePhotoCounter(){
            textPhotoCounter.visible = false
            textPhotoNum.visible = false
        }
    

        function onFlashIcon(code){
            if (code == "yes"){
                checkMark.visible = true;
                checkMarkTimer.restart()
            }
            else if (code == "no"){
                redX. visible = true;
                redXTimer.restart()
            }
            else if (code == "back"){
                backArrow.visible = true;
                backArrowTimer.restart()
            }
        }

        

        
    }


    Rectangle {
        id: page
        anchors.fill: parent
        color: "lightgray"
        
        Rectangle {
            id: photoHolder
            width: page.width
            height: page.height - 40
            anchors.top: page.top
            color: "#b7d1b6"

            Image {
                id: photo
                width: page.width
                height:parent.height
                fillMode: Image.PreserveAspectFit
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter

                Screen_Tutorial_Keys {
                }

                Screen_LoadFolder {
                }

                Screen_CameraAndLocationForm {
                }

                Screen_PrintReport {
                }

                Screen_NextCategory {
                }

                

                Keys.onPressed: (event)=> { 
                    //console.log("Key pressed: " + event.key)
                    if (event.key == Qt.Key_L){
                        slotBridge.choiceMade("yes") 
                    }
                    if (event.key == Qt.Key_Semicolon){
                        slotBridge.choiceMade("no")
                    } 
                    if (event.key == Qt.Key_Apostrophe){ 
                        slotBridge.choiceMade("back")
                    }
                    
                    if (event.key == Qt.Key_Return || event.key == Qt.Key_Enter){
                        if (!notesPopup.opened){
                            var note = slotBridge.getNote()
                            if (note != "NULL"){ //TODO: implement proper
                                var categoryData = slotBridge.getDataForPhoto()
                                console.log("categoryData " + categoryData) 
                                categoryCheckboxHolder.fillCategoryCheckboxes(categoryData)
                                
                                notesPopup.open()
                                notes.text = slotBridge.getNote() 

                                notes.lastFocus = window.activeFocusItem
                                notes.forceActiveFocus()
                            }
                        }
                    }

                    if (event.key == Qt.Key_Q) 
                    {
                        //console.log(focus)
                        //Test things here
                    }
                }
            }
        }

        Rectangle {
            id: infoBar
            width: page.width
            anchors.bottom: page.bottom
            height: 40
            color:"lightgrey"

            Text {
                id: textPhotoNum
                text: qsTr("Photo Num: ")
                height: 30
                anchors.right: textPhotoCounter.left
                anchors.verticalCenter: parent.verticalCenter
                rightPadding: 5
                font.pointSize: 24;
                visible: false
            }

            Text {
                id: textPhotoCounter
                text: qsTr("-/-")
                height: 30
                anchors.right: infoBar.right
                anchors.verticalCenter: parent.verticalCenter
                rightPadding: 5
                font.pointSize: 24; font.bold: true
                visible: false
            }

            Text {
                id: textIsThereA
                text: qsTr("Is there: ")
                height: 30
                anchors.left: infoBar.left
                anchors.verticalCenter: parent.verticalCenter
                leftPadding: 5
                font.pointSize: 24;
                visible: false
            }

            Text {
                id: textCategory
                text: qsTr("...?")
                height: 30
                anchors.left: textIsThereA.right
                anchors.verticalCenter: parent.verticalCenter
                leftPadding: 5
                font.pointSize: 24; font.bold: true
                visible: false
            }
        }

        Image {
            id:checkMark
            source: "AppImages/check-mark.png"
            anchors.horizontalCenter: page.horizontalCenter
            anchors.verticalCenter: page.verticalCenter
            height: page.height * 0.5
            width: page.height * 0.5
            visible: false

            Timer {
                id: checkMarkTimer
                interval: 100; 
                onTriggered: parent.visible = false;
            }
        }

        Image {
            id:redX
            source: "AppImages/x-circle.png"
            anchors.horizontalCenter: page.horizontalCenter
            anchors.verticalCenter: page.verticalCenter
            height: page.height * 0.5
            width: page.height * 0.5
            visible: false

            Timer {
                id:redXTimer
                interval: 100; 
                onTriggered: parent.visible = false;
            }
        }

        Image {
            id:backArrow
            source: "AppImages/left-arrow.png"
            anchors.horizontalCenter: page.horizontalCenter
            anchors.verticalCenter: page.verticalCenter
            height: page.height * 0.5
            width: page.height * 0.5
            visible: false

            Timer {
                id:backArrowTimer
                interval: 100; 
                onTriggered: parent.visible = false;
            }
        }

        Popup {
            id: notesPopup
            width: page.width - 20
            y: page.height - 100
            x:10

            CategoryBoxHolder {
                id: categoryCheckboxHolder
                anchors.bottom: spacer.top
                
            }

            Item {
                id: spacer
                height: 20
                anchors.bottom: notes.top
            }

            

            contentItem: TextField {
                id: notes
                placeholderText: qsTr("Put notes here...")
                wrapMode: Text.WordWrap
                focus:true

                property var lastFocus

                Keys.onPressed: (event)=> {
                    if ((event.key == Qt.Key_Return || event.key == Qt.Key_Enter) && notesPopup.opened) 
                    {
                        slotBridge.setNote(notes.text)

                        notes.text = ""
                        notesPopup.close()

                        lastFocus.forceActiveFocus()
                    }
                }
            }
        }
        
    }
}
