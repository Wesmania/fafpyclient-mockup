import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Controls.Material 2.13
import QtQuick.Layouts 1.3

MainWindowForm {
    logoutButton.onClicked: faf__session__login.logout()
}
