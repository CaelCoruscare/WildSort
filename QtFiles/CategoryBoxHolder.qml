import QtQuick
import QtQuick.Controls
import QtQuick.Layouts 1.14

ColumnLayout{
    id: head

    property var listOfCheckboxes: []

    function fillCategoryCheckboxes(listOfCheckedOrNot){
        for (var i = 0; i < listOfCheckedOrNot.length; i++) {
                var value = listOfCheckedOrNot[i]
                var box = listOfCheckboxes[i]
                console.log("|box|: " + i + "|value|: " + value)


            switch(value) {
                case 1:
                    console.log("TRUE")
                    box.enabled = true
                    box.checked = true
                    break;
                case 0:
                    console.log("FALSE")
                    box.enabled = true
                    box.checked = false
                    break;
                case "skip":
                    console.log("SKIPPED")
                    box.enabled = true
                    box.checked = false
                    break;
                default:
                    console.log("NONE")
                    box.checked = false
                    box.enabled = false
            }
        }
            
    }

    Connections{
        target: emitterBridge

        function onCreateCategoryCheckboxes(listOfCategories){
            var component = Qt.createComponent("CategoryBox.qml");

            for (var i = 0; i < listOfCategories.length; i++){
                var checkBox = component.createObject(head)
                checkBox.text = listOfCategories[i]
                checkBox.categoryIndex = i

                listOfCheckboxes.push(checkBox)
            }
        }
    }
}   