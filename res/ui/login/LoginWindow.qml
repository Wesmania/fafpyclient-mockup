import QtQuick 2.4

import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Controls.Material 2.13
import QtQuick.Layouts 1.3

LoginWindowForm {
    loginButton.onPressed: faf__server__login.login(loginTextbox.text, passwordTextbox.text)
}

