import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3

Item {
    property var fafChat
    property var chatModel
    property alias chatTabBar: chatTabBar
    property alias chatTabBarRepeater: chatTabBarRepeater
    property alias chatInputBox: chatInputBox
    
    fafChat: faf__tabs__chat
    chatModel: faf__tabs__chat__model

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
            }
        }
    }

    TextInput {
        id:  chatInputBox
        width: parent.width
        height: 20
        anchors.bottom: parent.bottom
	font.pointSize: 12
	onAccepted: {
            var currentTab = chatTabBar.currentItem;
            var channelName;
            var isPublic;
            if (currentTab === null) {
                channelName = null;
                isPublic = null;
            } else {
                channelName = currentTab.channelName;
                isPublic = currentTab.isPublic;
            }
            fafChat.send_message(channelName, isPublic, chatInputBox.text);
            chatInputBox.clear()
	}
    }
}
