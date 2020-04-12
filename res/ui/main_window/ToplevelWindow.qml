import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Controls.Material 2.13

ApplicationWindow {
    readonly property string iconPath: ROOT_PATH + "/res/icons/main_window/"
    id: mainWindow
    visible: true
    width: 1200
    height: 900

    Material.theme: Material.Dark
    Material.accent: Material.Grey
    font.capitalization: Font.MixedCase

    ToplevelWindowForm {
        id: mainWindowForm
        anchors.fill: parent
        function setLoginPane(logged_in) {
            currentIndex = logged_in ? 1 : 0
        }
    }

    Component.onCompleted: {
        loginController.loginSignal.connect(mainWindowForm.setLoginPane)
    }
}
