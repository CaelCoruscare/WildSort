import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    id: head
    border.color:"#B942EC"
    height: nextCategoryText.height + nextCategoryTextPrepend.height + 18
    width: page.width * 0.20 + 20
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    visible: false

    ShowerHider {
        code: "screen_nextcategory"
    }

    Connections{
        target: emitterBridge

        function onShowNextCategoryExplanation(text){
            nextCategoryText.text = "Next category: <b>" + text + "</b>"
            head.visible = true
            head.forceActiveFocus()
        }
    }

    Keys.onPressed: (event)=> { 
        if (event.key == Qt.Key_K){
            slotBridge.choiceMade("continue")
        }
    }

    ColumnLayout{

        Text {
            id: nextCategoryText
            text: qsTr("...?")
            topPadding: 10
            leftPadding: 5
            font.pointSize: 18
        }

        Text {
            id: nextCategoryTextPrepend
            text: qsTr("Press the <b><font color=\"#B942EC\">[K]</font></b> key to continue")
            font.pointSize: 14
            leftPadding: 5
        }
    }
}