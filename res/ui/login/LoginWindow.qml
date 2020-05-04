import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3

Item {
    property var fafLogin: faf__session__login
    function login() {
        var login = loginTextbox.text;
        var password = passwordTextbox.text;
        // TODO will have to clear this whenever login form is shown anew
        passwordTextbox.clear();
        fafLogin.login(login, password);
    }

    Column {
        anchors.centerIn: parent
        id: loginPane
        width: 300

        Image {
            id: loginImage
            anchors.horizontalCenter: parent.horizontalCenter
            width: 100
            height: 100
            fillMode: Image.PreserveAspectFit
        }

        TextField {
            id: loginTextbox
            anchors.left: parent.left
            anchors.right: parent.right
	    selectByMouse: true
	    onAccepted: passwordTextbox.focus = true
        }

        TextField {
            id: passwordTextbox
            echoMode: TextInput.Password
            anchors.left: parent.left
	    anchors.right: parent.right
	    onAccepted: login()
        }

        CheckBox {
            id: rememberLoginCheckbox
            anchors.right: parent.right
            text: qsTr("Automatic login")
        }

        Button {
            id: loginButton
            anchors.left: parent.left
            anchors.right: parent.right
            text: qsTr("Login")
            onAccepted: login()
        }

        RowLayout {
            anchors.left: parent.left
            anchors.right: parent.right

            Button {
                id: forgotLoginButton
                text: qsTr("Forgot login")
                Layout.fillWidth: true
                Layout.preferredWidth: 1
            }

            Button {
                id: createAccountButton
                text: qsTr("Create account")
                Layout.fillWidth: true
                Layout.preferredWidth: 1
            }
        }
    }
}
