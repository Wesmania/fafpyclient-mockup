import QtQuick 2.4

import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Controls.Material 2.13
import QtQuick.Layouts 1.3

LoginWindowForm {
    function login() {
        var login = loginTextbox.text;
        var password = passwordTextbox.text;
        // TODO will have to clear this whenever login form is shown anew
        passwordTextbox.clear();
        faf__session__login.login(login, password);
    }
    loginTextbox.onAccepted: passwordTextbox.focus = true
    passwordTextbox.onAccepted: login()
    loginButton.onPressed: login()
}

