import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

ColumnLayout{
    id: head
    anchors.verticalCenter: parent.verticalCenter
    anchors.horizontalCenter: parent.horizontalCenter
    visible: false

    Focuser {
        code: "screen_printreport"
    }

    ShowerHider {
        code: "screen_printreport"
    }

    //This just prevents any input from being registered unless the button is clicked.
    Keys.onPressed: (event)=> { 
        console.log("Key pressed from Screen_PrintReport: " + event.key)

        event.accepted = true //Prevent key event from being handled again at base
    }

    Button {
        id: printButton
        text: qsTr("Print Report")
        Layout.alignment: Qt.AlignCenter
        
        onClicked: {
            slotBridge.printReport();
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