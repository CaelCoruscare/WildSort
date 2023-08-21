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
        function onShowFolderSelectionArea(){
            folderSelectionArea.visible = true
        }
        function onHideFolderSelectionArea(){
            folderSelectionArea.visible = false
        }
        function onShowNextCategoryExplanation(text){
            nextCategoryText.text = text
            nextCategoryArea.visible = true
        }
        function onHideNextCategoryExplanation(){
            nextCategoryArea.visible = false
        }
        function onShowExplanation(text){
            genericExplanationText.text = text
            genericExplanation.visible = true
        }
        function onHideExplanation(){
            genericExplanation.visible = false
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
                focus:true

                ColumnLayout{
                    id: folderSelectionArea
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    
                    Button {
                        id: folderButton
                        text: qsTr("Select Folder")
                        Layout.alignment: Qt.AlignCenter
                        
                        onClicked: {
                            folderDialog.open();
                            folderSelectionArea.visible = false;
                        }
                    }

                    Rectangle {
                        border.color:"green"
                        Layout.minimumHeight: explanation.height + 20  
                        Layout.preferredWidth: page.width * 0.3 + 20

                        Text {
                            id: explanation
                            text: "Load a folder of photos from a single camera trap.\n\nThis program will sort all the photos into categories. For any photos where the AI is not sure, it will ask you for help. Your answers will be used to train the AI for future runs.\n\nPlease note that the AI will take a lot of training before it functions well. "
                            wrapMode: Text.WordWrap
                            width: page.width * 0.3
                            anchors.horizontalCenter: parent.horizontalCenter
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }

                Rectangle {
                    id: genericExplanation
                    border.color:"orange"
                    height: nextCategoryText.height + 20  
                    width: page.width * 0.30 + 20
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    visible: false

                    Text {
                        id: genericExplanationText
                        text: "Generic"
                        wrapMode: Text.WordWrap
                        width: page.width * 0.30
                        anchors.horizontalCenter: parent.horizontalCenter
                        anchors.verticalCenter: parent.verticalCenter
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                Rectangle {
                    id: nextCategoryArea
                    //border.color:"blue"
                    height: nextCategoryText.height + 20  
                    width: page.width * 0.20 + 20
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    visible: false

                    Text {
                        id: nextCategoryTextPrepend
                        text: qsTr("Next category:")
                        wrapMode: Text.WordWrap
                        anchors.verticalCenter: parent.verticalCenter
                        horizontalAlignment: Text.AlignHCenter
                        font.pointSize: 18;
                        leftPadding: 5
                    }

                    Text {
                        id: nextCategoryText
                        text: qsTr("...?")
                        anchors.left: nextCategoryTextPrepend.right
                        anchors.verticalCenter: parent.verticalCenter
                        leftPadding: 5
                        font.pointSize: 18; font.bold: true
                    }
                }

                Keys.onPressed: (event)=> { 
                    if (event.key == Qt.Key_L){
                        slotBridge.choiceMade("yes"); 
                    }
                    if (event.key == Qt.Key_Semicolon){
                        slotBridge.choiceMade("no"); 
                    } 
                    if (event.key == Qt.Key_Apostrophe){ 
                        slotBridge.choiceMade("back"); 
                    }

                    if (event.key == Qt.Key_Return) 
                    {
                        if (!popup.opened)
                        {
                            popup.open();
                            notes.text = slotBridge.getNote() ;
                            notes.forceActiveFocus();
                        }
                    }
                }
            }
           
            FolderDialog {
                id: folderDialog
                currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
                onAccepted: {
                    slotBridge.folderChosen(selectedFolder);
                    currentFolder = selectedFolder;
                    folderSelectionArea.visible = false;
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
            id: popup
            //anchors.centerIn: parent 
            width: page.width - 20
            y: page.height - 100
            x:10

            contentItem: TextField {
                id: notes
                placeholderText: qsTr("Put notes here...")
                wrapMode: Text.WordWrap
                //anchors.bottom: page.bottom
                //anchors.horizontalCenter: page.horizontalCenter
                focus:true
                Keys.onPressed: (event)=> {
                    if (event.key == Qt.Key_Return && popup.opened) 
                    {
                        slotBridge.setNote(notes.text);
                        notes.text = "";
                        photo.forceActiveFocus()
                        popup.close();
                    }
                }
            }
        } 
    }
}
