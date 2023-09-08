import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ColumnLayout{
    id: head
    anchors.top: parent.top
    anchors.horizontalCenter: parent.horizontalCenter
    height: parent.height * 0.65
    visible: false

    ShowerHider {
        code: "tutorial_keys"
    }

    Focuser {
        code: "tutorial_keys"
    }

    Keys.onPressed: (event)=> { 
        if (event.key == Qt.Key_K){
            slotBridge.choiceMade("continue")
        }
    }

    Image {
        id: keysTutorial_Pic
        source: "AppImages/tutorial-keys.png"
        fillMode: Image.PreserveAspectFit
        Layout.alignment: Qt.AlignCenter
        Layout.fillHeight: true
    }

    Rectangle {
        id: keysTutorial_Rect
        border.color:"green"
        Layout.preferredHeight: keysTutorial_Text.implicitHeight + 20 
        Layout.preferredWidth: keysTutorial_Text.implicitWidth + 20
        Layout.alignment: Qt.AlignCenter

        Text {
            id: keysTutorial_Text
            text: "Use the <b><font color=\"green\">[L]</font></b> and <b><font color=\"red\">[;]</font></b> keys as <b><font color=\"green\">Yes</font></b> and <b><font color=\"red\">No</font></b>, to Sort the Photos.<br><br>Use the <b><font color=\"blue\">[']</font></b> key to go <b><font color=\"blue\">Back</font></b> to the previous Photo.<br><br>Use the <b><font color=\"#E19133\">[return]</font></b> or <b><font color=\"#E19133\">[Enter]</font></b> key to open <b><font color=\"#E19133\">Notes</font></b>.<br><br>Press the <b><font color=\"#B942EC\">[K]</font></b> key to start sorting."
            wrapMode: Text.WordWrap
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
        }
    }

}