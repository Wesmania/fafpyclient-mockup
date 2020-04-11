import QtQuick 2.4
import QtQuick.Controls 2.13

TabButton {
    id: mainTabButton
    property alias icon_s: mainTabButton.icon.source
    width: implicitWidth
    anchors.verticalCenter: parent.verticalCenter
}
