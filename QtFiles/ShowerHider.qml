import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

Item {
    id: head
    property string code

    Connections {
        target: emitterBridge 

        function onShowElement(c){
            if (code == c)
                head.parent.visible = true
        }

        function onHideElement(c){
            if (code == c)
                head.parent.visible = false
        }
    }
}