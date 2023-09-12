import QtQuick
import QtQuick.Controls
import QtQuick.Layouts 1.14

ColumnLayout{
    id: head

    property var listOfCheckboxes: []

    function fillCategoryCheckboxes(listOfCheckedOrNot){
        for (var i = 0; i < listOfCheckedOrNot.length; i++) {
                console.log("||: " + listOfCheckedOrNot[i])
            switch(listOfCheckedOrNot[i]) {
                case 1:
                    console.log("TRUE")
                    listOfCheckboxes[i].enabled = true
                    listOfCheckboxes[i].checked = true
                    break;
                case 0:
                    console.log("FALSE")
                    listOfCheckboxes[i].enabled = true
                    listOfCheckboxes[i].checked = false
                    break;
                case "skip":
                    console.log("SKIPPED")
                    listOfCheckboxes[i].enabled = true
                    listOfCheckboxes[i].checked = false
                    break;
                default:
                    console.log("NONE")
                    listOfCheckboxes[i].enabled = false
                    listOfCheckboxes[i].checked = false
            }
            listOfCheckboxes[i].checked = listOfCheckedOrNot[i];
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