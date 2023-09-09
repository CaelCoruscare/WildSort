import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ColumnLayout{
    id: head
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    visible: false

    ShowerHider {
        code: "screen_printreport"
    }

    Focuser {
        code: "screen_printreport"
    }
    
    Button {
        id: printButton
        text: qsTr("Print Report")
        Layout.alignment: Qt.AlignCenter
        
        onClicked: {
            slotBridge.printReport();
            head.visible = false;
        }
    }

    Rectangle {
        border.color:"green"
        Layout.minimumHeight: printReportExplanation.height + 20  
        Layout.preferredWidth: page.width * 0.3 + 20

        Text {
            id: printReportExplanation
            text: "Report is ready to print."
            wrapMode: Text.WordWrap
            width: page.width * 0.3
            anchors.horizontalCenter: parent.horizontalCenter
            anchors.verticalCenter: parent.verticalCenter
        }
    }
}