import QtQuick
import QtQuick.Controls
import QtQuick.Layouts 1.14

ColumnLayout{
    id: head

    property var listOfCheckboxes: []

    function fillCategoryCheckboxes(listOfCheckedOrNot){
        for (var i = 0; i < listOfCheckedOrNot.length; i++) {
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