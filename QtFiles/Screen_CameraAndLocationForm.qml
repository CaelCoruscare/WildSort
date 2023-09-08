import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ColumnLayout {
    id: top
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    visible: false
    focus: true

    ShowerHider {
        code: "screen_cameralocation"
    }

    Keys.onPressed: (event)=> { 
        if (event.key == Qt.Key_Return || event.key == Qt.Key_Enter) {
            formSubmitted()
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
        slotBridge.choiceMade("continue")
    }

    Text {
        text: qsTr("Camera Used")
    }
    TextField {
        id: cameraField
        text: qsTr("This should be filled by SlotBridge.SetFolder()")
    }
    
    Text {
        text: qsTr("Location")
    }
    TextField {
        id: locationField
        focus:true
        Keys.forwardTo: [cameraAndLocationButton]

        Focuser {
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