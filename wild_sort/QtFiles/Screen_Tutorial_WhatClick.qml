import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ColumnLayout{
    id: head
    anchors.top: parent.top
    anchors.horizontalCenter: parent.horizontalCenter
    height: parent.height * 0.95
    visible: false

    Focuser{
        code: "screen_tutorial_whatclick"
    }

    ShowerHider {
        code: "screen_tutorial_whatclick"
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