import QtQuick 2.4

ChatTabForm {
    property var chat

    chat: faf__tabs__chat
    chatModel: faf__tabs__chat__model

    Connections {
        target: channelTabBarButtons
        onItemAdded: {
            item.quit.connect(function(channelName, isPublic){
                chat.leave_channel(channelName, isPublic);
             })
        }
    }
}
