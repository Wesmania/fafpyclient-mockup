import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3
import "../login"

ToplevelWindowTempl {
    id: mainWindow
    property var fafLogin

    fafLogin: faf__session__login

    StackLayout {
        id: mainWindowForm
        anchors.fill: parent
	currentIndex: 0
	LoginWindow {

	}
	MainWindow {

	}
        function showLoginPane() {
            currentIndex = 0
        }

        function hideLoginPane() {
            currentIndex = 1
        }
    }

    Component.onCompleted: {
        fafLogin.logged_in.connect(mainWindowForm.hideLoginPane)
        fafLogin.logged_out.connect(mainWindowForm.showLoginPane)
    }
}
