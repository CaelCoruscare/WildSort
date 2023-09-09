import QtQuick
import QtQuick.Controls

CheckBox {
    property int categoryIndex
    checked: false

    onToggled: {
        slotBridge.flipValueInCategory(categoryIndex)
    }
}