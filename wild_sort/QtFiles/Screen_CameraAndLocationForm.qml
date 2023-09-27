import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ColumnLayout {
    id: top
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    visible: false

    ShowerHider {
        code: "screen_cameralocation"
    }

    Keys.onPressed: (event)=> { 
        console.log("Key pressed from Screen_CamLoc: " + event.key)

        if (event.key == Qt.Key_Return || event.key == Qt.Key_Enter) {
            formSubmitted()

            event.accepted = true
        }
    }

    
    Connections {
        target: emitterBridge
        function onFillCamAndLocForm(camera, location){
            cameraField.text = camera
            locationField.text  = location
        }
    }

    function formSubmitted(){
        slotBridge.setCameraAndLocation(cameraField.text, locationField.text)
        slotBridge.nextScreen()
    }

    Text {
        text: qsTr("Camera Used")
    }
    TextField {
        id: cameraField
        text: qsTr("This should be filled by SlotBridge.SetFolder()")

        Setter{
            code: "field_camera"
            property alias prop: cameraField.text
        }
    }
    
    Text {
        text: qsTr("Location")
    }
    TextField {
        id: locationField
        //Keys.forwardTo: [cameraAndLocationButton]

        Setter{
            code: "field_location"
            property alias prop: locationField.text
        }

        Focuser {
            id: locationField_Focuser
            code: "field_location"
        }
    }

    Button {
        id: cameraAndLocationButton
        text: qsTr("Confirm")
        Layout.alignment: Qt.AlignCenter
        
        onClicked: {
            formSubmitted()
        }
    }
}