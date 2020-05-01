import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Controls.Material 2.13

ToplevelWindowTempl {
    id: mainWindow

    ToplevelWindowForm {
        id: mainWindowForm
        anchors.fill: parent
        function showLoginPane() {
            currentIndex = 0
        }

        function hideLoginPane() {
            currentIndex = 1
        }
    }

    Component.onCompleted: {
        faf__session__login.logged_in.connect(mainWindowForm.hideLoginPane)
        faf__session__login.logged_out.connect(mainWindowForm.showLoginPane)
    }
}
