import QtCore
import QtQuick
import QtQuick.Window
import QtQuick.Controls
import QtQuick.Dialogs
import Qt.labs.folderlistmodel 2.5
import QtQuick.Layouts

import io.qt.textproperties 1.0



Window {
    width: 640
    height: 480
    visible: true
    title: qsTr("Hello World")

   


    Connections{
        target: imageLogic
        function onLooking4Changed(newType){
            textType.text = newType + "?"
        }
        function onPictureChanged(picOnOf){
            textPhotoNum.text = picOnOf
        }
    }

    ImageLogic {
        id: imageLogic
    }

    
    
        //focusPolicy: Qt.NoFocus


    Rectangle {
        id: page
        anchors.fill: parent
        color: "lightgray"
        
        Rectangle {
            id: imageHolder
            width: page.width
            height: page.height - 40
            anchors.top: page.top
            color: "green"

           Image {
                id: image
                width: page.width
                height:parent.height
                fillMode: Image.PreserveAspectFit
                anchors.verticalCenter: parent.verticalCenter
                anchors.horizontalCenter: parent.horizontalCenter
                focus:true
                Keys.onPressed: (event)=> { 
                    if (event.key == Qt.Key_L) source = imageLogic.choiceMade("yes");  
                    else if (event.key == Qt.Key_Semicolon) source = imageLogic.choiceMade("no"); 
                    else if (event.key == Qt.Key_Apostrophe) source = imageLogic.choiceMade("back"); 

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
           }
           

            FolderDialog {
                id: folderDialog
                currentFolder: StandardPaths.standardLocations(StandardPaths.PicturesLocation)[0]
                //selectedFolder: viewer.folder
                onAccepted: image.source = imageLogic.setFolder(selectedFolder)
            }

            Button {
                text: qsTr("Select File")
                onClicked: folderDialog.open()
                //onClicked: popup.open()
                
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
                text: "Is there: "
                height: 30
                anchors.left: infoBar.left
                anchors.verticalCenter: parent.verticalCenter
                leftPadding: 5
                font.pointSize: 24;
            }

            Text {
                id: textType
                text: "...?"
                height: 30
                anchors.left: textIsThereA.right
                anchors.verticalCenter: parent.verticalCenter
                leftPadding: 5
                font.pointSize: 24; font.bold: true
            }

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
            placeholderText: "Put notes here..."
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
