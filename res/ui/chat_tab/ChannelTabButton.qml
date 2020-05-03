import QtQuick 2.4
import QtQuick.Controls 2.13

ChannelTabButtonForm {
    property string channelName
    property bool isPublic

    text: channelName

    Connections {
        target: channelTabQuitButton
        onPressed: {
            fafChat.leave_channel(channelName, isPublic)
        }
    }
}
