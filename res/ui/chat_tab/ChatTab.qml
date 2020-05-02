import QtQuick 2.4

ChatTabForm {
    property var chat

    chat: faf__tabs__chat
    chatModel: faf__tabs__chat__model

    Connections {
        target: chatTabBarRepeater
        onItemAdded: {
            item.quit.connect(function(channelName, isPublic) {
                chat.leave_channel(channelName, isPublic);
             })
        }
    }

    Connections {
        target: chatInputBox
        onAccepted: {
            var currentTab = chatTabBar.currentItem;
            if (currentTab === undefined) {
                return;
            }
            var channelName = currentTab.channelName;
            var isPublic = currentTab.isPublic;
            chat.send_message(channelName, isPublic, chatInputBox.text);
            chatInputBox.text = ""
        }
    }
}
