ColumnLayout{
    id: folderSelectionArea
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter

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

    Button {
        id: folderButton
        text: qsTr("Select Folder")
        Layout.alignment: Qt.AlignCenter
        
        onClicked: {
            folderDialog.open();
            folderSelectionArea.visible = false;
        }
    }
}