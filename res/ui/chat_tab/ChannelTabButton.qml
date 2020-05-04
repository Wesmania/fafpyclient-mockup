import QtQuick 2.4
import QtQuick.Controls 2.13

TabButton {
    id: tabButton
    text: channel_name

    contentItem: Row {
        Text {
            id: buttonText
            height: parent.height
            text: tabButton.text
            font: tabButton.font
        }
        Button {
            id: channelTabQuitButton
            icon {
               source: ROOT_PATH + "/res/icons/general/close.svg"
            }
            width: parent.height
            height: parent.height
            display: AbstractButton.IconOnly
	    flat: true
	    onPressed: fafChat.leave_channel(channel_name, is_public)
        }
    }
}
