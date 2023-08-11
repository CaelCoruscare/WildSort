import QtCore
import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Dialogs
import Qt.labs.folderlistmodel 2.5
import QtQuick.Layouts

import io.qt.textproperties 1.0



Window {
    width: 1280
    height: 640
    visible: true
    title: qsTr("WildSort")

   


    Connections{
        target: imageLogic
        function onLooking4Changed(newType){
            textType.text = newType + "?"
        }
        function onPictureChanged(picOnOf){
            textPhotoNum.text = picOnOf
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
            else if (code == "typechange"){
                redX. visible = false;
                checkMark.visible = false;
                typeChangeArrow.visible = true;
                typeChangeArrowTimer.restart()
            }
        }
    }

    ImageLogic {
        id: imageLogic
    }

    Rectangle {
        id: page
        anchors.fill: parent
        color: "lightgray"
        
        Rectangle {
            id: imageHolder
            width: page.width
            height: page.height - 40
            anchors.top: page.top
            color: "#b7d1b6"

           Image {
                id: image
                width: page.width
                height:parent.height
                fillMode: Image.PreserveAspectFit
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                focus:true
                Keys.onPressed: (event)=> { 
                    if (event.key == Qt.Key_L){
                        imageSourceHolder.text = imageLogic.choiceMade("yes"); 
                        imageTimer.restart();
                    }
                    if (event.key == Qt.Key_Semicolon){
                        imageSourceHolder.text = imageLogic.choiceMade("no"); 
                        imageTimer.restart();
                    } 
                    if (event.key == Qt.Key_Apostrophe){ 
                        imageSourceHolder.text = imageLogic.choiceMade("back"); 
                        imageTimer.restart();
                    }

                    if (event.key == Qt.Key_Return) 
                    {
                        if (!popup.opened)
                        {
                            popup.open();
                            notes.text = imageLogic.getNote() 
                            notes.forceActiveFocus();
                        }
                    }
                        
                }
                
                Timer {
                    id:imageTimer
                    interval: 200; 

                    onTriggered: parent.source = imageSourceHolder.text;

                    
                }
                TextField {
                    id: imageSourceHolder;
                    visible: false;
                    text: "Hello";
                }
           }
           

            FolderDialog {
                id: folderDialog
                currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
                //selectedFolder: viewer.folder
                onAccepted: image.source = imageLogic.setFolder(selectedFolder)
            }

            Button {
                id: folderButton
                text: qsTr("Select Folder")
                onClicked: {
                    folderDialog.open();
                    folderButton.visible = false;
                }
                
            }


            FileDialog {
                id: fileDialog
                //currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
                onAccepted: image.source = selectedFile
                //onAccepted: imageHolder.color = imageLogic.getColor(imageLogic.testColor)
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
                text: "Photo 0/0"
                height: 30
                anchors.right: infoBar.right
                anchors.verticalCenter: parent.verticalCenter
                rightPadding: 5
                font.pointSize: 24; font.bold: true
            }

            Text {
                id: textIsThereA
                text: qsTr("Is there: ")
                height: 30
                anchors.left: infoBar.left
                anchors.verticalCenter: parent.verticalCenter
                leftPadding: 5
                font.pointSize: 24;
            }

            Text {
                id: textType
                text: qsTr("...?")
                height: 30
                anchors.left: textIsThereA.right
                anchors.verticalCenter: parent.verticalCenter
                leftPadding: 5
                font.pointSize: 24; font.bold: true
            }

        }

    }

    Image {
        id:checkMark
        source: "images/check-mark.png"
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
        source: "images/x-circle.png"
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
        source: "images/left-arrow.png"
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

    Image {
        id:typeChangeArrow
        source: "images/restart-arrow.png"
        anchors.horizontalCenter: page.horizontalCenter
        anchors.verticalCenter: page.verticalCenter
        height: page.height * 0.8
        width: page.height * 0.8
        visible: false

        Timer {
            id:typeChangeArrowTimer
            interval: 1000; 
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
                    imageLogic.recordNote(notes.text);
                    notes.text = "";
                    image.forceActiveFocus()
                    popup.close();
                }
            }
        }
    } 
    
}
