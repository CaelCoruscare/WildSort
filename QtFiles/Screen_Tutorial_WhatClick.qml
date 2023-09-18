import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ColumnLayout{
    id: head
    anchors.top: parent.top
    anchors.horizontalCenter: parent.horizontalCenter
    height: parent.height * 0.95
    visible: false

    ShowerHider {
        code: "tutorial_whatclick"
    }

    Focuser {
        code: "tutorial_whatclick"
    }

    Keys.onPressed: (event)=> { 
        if (event.key == Qt.Key_K){
            slotBridge.choiceMade("continue")
        }
    }

    Image {
        id: keysTutorial_Pic
        source: "AppImages/tutorial-whatclick.png"
        fillMode: Image.PreserveAspectFit
        Layout.alignment: Qt.AlignCenter
        Layout.fillHeight: true
    }



    Image {
        id:explainerImage
        source: "AppImages/continue.png"
        fillMode: Image.PreserveAspectFit
        
        Layout.preferredHeight: 100
        Layout.alignment: Qt.AlignHCenter;
    }

}