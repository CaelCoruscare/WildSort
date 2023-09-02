import QtQuick

Item {
    id: categoryBox
    property alias cellColor: rectangle.color
    signal clicked(cellColor: color)

    width: checkBox.width; height: 25

    Rectangle {
        id: rectangle
        border.color: "white"
        anchors.fill: parent
    }

    MouseArea {
        anchors.fill: parent
        onClicked: container.clicked(container.cellColor)
    }

    CheckBox {
        checkBox
        checked: true
        text: qsTr("First")
        onToggled: {

        }
    }
}