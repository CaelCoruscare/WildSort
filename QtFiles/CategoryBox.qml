import QtQuick
import QtQuick.Controls

CheckBox {
    property int categoryIndex
    checked: false

    onToggled: {
        var newValues = slotBridge.flipValueInCategory(categoryIndex)
        parent.fillCategoryCheckboxes(newValues)
    }
}