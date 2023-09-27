import QtQuick
import QtQuick.Layouts
import QtQuick.Controls

//Focuses whatever it is attached to when onFocusElement(code) is called with the specified code

Item {
    id: head
    property string code
    property var lastFocus

    function releaseActiveFocus(){
            lastFocus.forceActiveFocus()
        }

    function focusTarget(){
        console.log("LastFocus: " + window.activeFocusItem)
        lastFocus = window.activeFocusItem
        head.parent.forceActiveFocus()
    }

    Connections {
        target: emitterBridge 

        function onFocusElement(c){
            if (code == c)
            {
                console.log("Focus Element is: " + code)
                focusTarget()
            }
        }
    }
}