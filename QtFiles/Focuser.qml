import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

//Focuses whatever it is attached to when onFocusElement(code) is called with the specified code

Item {
    id: head
    property string code

    Connections {
        target: emitterBridge 

        function onFocusElement(c){
            if (code == c)
                head.parent.forceActiveFocus()
        }
    }
}