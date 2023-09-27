import QtQuick

Item {
    id: head
    property string code

    Connections {
        target: emitterBridge 

        function onSetText(c, t){
            if (code == c)
                prop = t
        }
    }
}