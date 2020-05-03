import QtQuick 2.4
import QtQuick.Controls 2.13

ChannelTabButtonForm {
    property string channelName
    property bool isPublic
    signal quit(string channelName, bool isPublic)

    text: channelName

    Connections {
        target: channelTabQuitButton
        onPressed: {
            quit(channelName, isPublic)
        }
    }
}
