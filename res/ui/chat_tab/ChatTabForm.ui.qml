import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3

Item {
    property var chatModel
    property alias chatTabBar: chatTabBar
    property alias chatTabBarRepeater: chatTabBarRepeater
    property alias chatInputBox: chatInputBox
    id: chatFrame

    TabBar {
        id: chatTabBar
        width: parent.width
        anchors.top: parent.top
        Repeater {
            id: chatTabBarRepeater
            model: chatModel
            ChannelTabButton {
                width: implicitWidth
                id: chatTabBarButton
                channelName: channel_name
                isPublic: is_public
            }
        }
    }

    StackLayout {
        id: chatTabChannelStack
        width: parent.width
        anchors.top: chatTabBar.bottom
        anchors.bottom: chatInputBox.top
        currentIndex: chatTabBar.currentIndex

        Repeater {
            id: chatTabChannelTabs
            model: chatModel
            ChannelTab {
                isPublic: is_public
                channelTopic: channel_topic
                linesModel: lines_model
                chattersModel: chatters_model
            }
        }
    }

    TextInput {
        id:  chatInputBox
        width: parent.width
        height: 20
        anchors.bottom: parent.bottom
        font.pointSize: 12
    }
}
