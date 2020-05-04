import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.0
import '../news_tab'
import '../game_tab'
import '../chat_tab'

Item {
    property var fafSession: faf__session__login
    id: element
    width: 1200
    height: 900

    Item {
        id: menuBarPane
        height: 50
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.top: parent.top

        Image {
            id: menuButton
            source: iconPath + "minimize-button.png"	// FIXME
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.margins: 6
            fillMode: Image.PreserveAspectFit
            MouseArea {
                anchors.fill: parent
                // TODO: onClicked
            }
        }

        TabBar {
            id: clientTabBar
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: menuButton.right
            leftPadding: 6

            MainTabButton {
                id: newsButton
                text: qsTr("News")
                icon_s: iconPath + "feed.png"
            }

            MainTabButton {
                id: chatButton
                text: qsTr("Chat")
                icon_s: iconPath + "chat.png"
            }

            MainTabButton {
                id: playButton
                icon_s: iconPath + "games.png"
                text: qsTr("Play")
            }

            MainTabButton {
                id: vaultsButton
                icon_s: iconPath + "mods.png"
                text: qsTr("Vault")
            }

            MainTabButton {
                id: leaderboardsButton
                icon_s: iconPath + "ladder.png"
                text: qsTr("Leaderboards")
            }

            MainTabButton {
                id: unitdbButton
                icon_s: iconPath + "unitdb.png"
                text: qsTr("Units")
            }
        }

        Button {
            id: logoutButton
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.right: parent.right
            text: qsTr("Logout")
	    onClicked: fafSession.logout()
        }
    }

    StackLayout {
        id: clientTabs
        anchors.top: menuBarPane.bottom
        anchors.right: parent.right
        anchors.left: parent.left
        anchors.bottom: parent.bottom
        currentIndex: clientTabBar.currentIndex

        News {

        }
        ChatTab {

        }
        GameTab {

        }
    }
}
