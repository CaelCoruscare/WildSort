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
        focus: true

        Keys.onPressed: (event)=> { 
                console.log("Key pressed from Wildsort: " + event.key)

                if (event.key == Qt.Key_K){ 
                    slotBridge.nextScreen()
                }
                if (event.key == Qt.Key_Apostrophe){ 
                    slotBridge.previousScreen()
                }
                

                if (event.key == Qt.Key_Q) 
                {
                    testPopup.open()
                    //console.log(focus)
                    //Test things here
                }
            }
        
        Rectangle {
            id: photoHolder
            width: page.width
            height: page.height - 40
            anchors.top: page.top
            color: "#b7d1b6"

            Screen_ImageViewer {
            }

            Screen_ChooseFolder {
            }

            Screen_CameraAndLocationForm {
            }

            Screen_Tutorial_Keys {
            }

            Screen_Tutorial_WhatClick {
            }

            Screen_PrintReport {
            }

            Screen_NextCategory {
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
                ShowerHider {
                    code: "text_photocounter"
                }
                Setter {
                    code: "text_photocounter"
                    property alias prop: textPhotoCounter.text
                }
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
                ShowerHider {
                    code: "text_categoryis"
                }
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
                ShowerHider {
                    code: "text_categoryis"
                }
                Setter{
                    code: "text_categoryis"
                    property alias prop: textCategory.text
                }
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
            id: testPopup
        }

        Popup {
            id: notesPopup
            width: page.width - 20
            height: page.height - 20
            x:10
            closePolicy: Popup.CloseOnEscape
            background: Rectangle{
                color: "transparent"
                //border.color: "black"
            }

            Rectangle{
                implicitWidth: 200 // <==
                implicitHeight: parent.height - 64
                anchors.top: parent.top

                color:"lightgrey"

                ScrollView {
                    implicitWidth: 200// <==
                    implicitHeight: parent.height - 16
                    y:8
                    // anchors.top: parent.top

                    CategoryBoxHolder {
                        id: categoryCheckboxHolder
                        implicitWidth: 200 // <==
                        implicitHeight: contentHeight
                    } 
                }   
            }

            TextField {
                id: notes
                placeholderText: qsTr("Put notes here...")
                wrapMode: Text.WordWrap
                y: page.height - 80
                focus:true

                //anchors.bottom: parent.bottom
                //bottomPadding: 50
                width: parent.width

                property var lastFocus

                Keys.onPressed: (event)=> {
                    console.log("Key pressed from Notes: " + event.key)

                    if ((event.key == Qt.Key_Return || event.key == Qt.Key_Enter) && notesPopup.opened) 
                    {
                        slotBridge.setNote(notes.text)

                        notes.text = ""
                        notesPopup.close()

                        lastFocus.forceActiveFocus()

                        event.accepted = true
                    }
                }
            }
            
        }
        
    }
}
