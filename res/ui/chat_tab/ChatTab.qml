import QtQuick 2.4

ChatTabForm {
    property var fafChat

    fafChat: faf__tabs__chat
    chatModel: faf__tabs__chat__model

    Connections {
        target: chatInputBox
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
