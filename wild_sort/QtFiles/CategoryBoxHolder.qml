import QtQuick
import QtQuick.Controls
import QtQuick.Layouts 1.14


ListView{
    id: head

    ListModel {
        id: mdl
        //Example:
        // ListElement {
        //     title: "Domestic Animal"
        //     _checked: false
        //     _enabled: true
        //     //categoryIndex: 3
        // }
    }

    model: mdl

    delegate: CategoryBox{text: title; checked: _checked; enabled: _enabled; categoryIndex: _categoryIndex; leftPadding: indentation }

    function fillCategoryCheckboxes(listOfCheckedOrNot){
        for (var i = 0; i < listOfCheckedOrNot.length; i++) {
                var value = listOfCheckedOrNot[i]
                var boxElement = mdl.get(i)



            switch(value) {
                case 1:
                    //console.log("TRUE")
                    boxElement._enabled = true
                    boxElement._checked = true
                    break;
                case 0:
                    //console.log("FALSE")
                    boxElement._enabled = true
                    boxElement._checked = false
                    break;
                case "skip":
                    //console.log("SKIPPED")
                    boxElement._enabled = true
                    boxElement._checked = false
                    break;
                default:
                    //console.log("NONE")
                    boxElement._checked = false
                    boxElement._enabled = false
            }
        }
            
    }

    Connections{
        target: emitterBridge

        function onCreateCategoryCheckboxes(listOfCategories, listOfIndentations){
            for (var i = 0; i < listOfCategories.length; i++){
                mdl.append({"title": listOfCategories[i], "_checked": false, "_enabled": true, "_categoryIndex": i, "indentation": listOfIndentations[i]*8})
            }
        }
    }
}   