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
	    var channelName;
	    var isPublic;
            if (currentTab === null) {
                channelName = null;
                isPublic = null;
            } else {
                channelName = currentTab.channelName;
                isPublic = currentTab.isPublic;
	    }
            chat.send_message(channelName, isPublic, chatInputBox.text);
            chatInputBox.clear()
        }
    }
}
