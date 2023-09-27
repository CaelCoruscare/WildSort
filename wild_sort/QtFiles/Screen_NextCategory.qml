import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Rectangle {
    id: head
    border.color:"#B942EC"
    height: nextCategoryText.height +  18
    width: page.width * 0.20 + 20
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    visible: false

    Focuser{
        code: "screen_nextcategory"
    }

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

    Text {
        id: nextCategoryText
        text: qsTr("...?")
        topPadding: 10
        leftPadding: 5
        font.pointSize: 18
        Setter{
            code: "text_nextcategory"
            property alias prop: nextCategoryText.text
        }
        ShowerHider {
            code: "text_nextcategory"
        }
    }

    Image {
        id: purpleCircleArrow
        width: page.width
        height:page.height
        fillMode: Image.PreserveAspectFit
        anchors.verticalCenter: parent.verticalCenter
        anchors.horizontalCenter: parent.horizontalCenter
        source: "AppImages/restart-arrow.png"
    }

    Image {
        id:explainerImage
        fillMode: Image.PreserveAspectFit
        
        source: "AppImages/continue.png"
        width: 265
        anchors.top: head.bottom
    }
}