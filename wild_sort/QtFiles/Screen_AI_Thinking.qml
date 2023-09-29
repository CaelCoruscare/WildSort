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
        code: "screen_ai_thinking"
    }

    ShowerHider {
        code: "screen_ai_thinking"
    }
    Image {
        id: keysTutorial_Pic
        source: "AppImages/ai-thinking.png"
        fillMode: Image.PreserveAspectFit
        Layout.alignment: Qt.AlignCenter
        Layout.fillHeight: true
    }

}