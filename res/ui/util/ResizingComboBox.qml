import QtQuick 2.9
import QtQuick.Controls 2.2

// https://stackoverflow.com/questions/45029968/how-do-i-set-the-combobox-width-to-fit-the-largest-item
ComboBox {
    property int textWidth

    implicitWidth: leftPadding + textWidth + indicator.width + rightPadding

    TextMetrics {
        id: popupMetrics
    }

    TextMetrics {
        id: textMetrics
    }

    // We call this every time the options change (and init)
    // so we can adjust the combo box width here too
    onActivated: resetWidth()

    function resetWidth() {
        textMetrics.font = font
        popupMetrics.font = popup.font
        textWidth = 0
        for (var i = 0; i < count; i++){
            textMetrics.text = textAt(i)
            popupMetrics.text = textAt(i)
            textWidth = Math.max(textMetrics.width, textWidth)
            textWidth = Math.max(popupMetrics.width, textWidth)
        }
    }

    Component.onCompleted: resetWidth()
}
