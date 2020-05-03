import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3

Item {
    property bool isPublic;
    property string channelTopic;
    property alias linesModel : linesView.model
    property alias chattersModel : chattersView.model

    Text {
        id: chatTopic
        width: parent.width
        anchors.top: parent.top
        text: channelTopic
    }

    SplitView {
        width: parent.width
        anchors.top: chatTopic.bottom
        anchors.bottom: parent.bottom
        ListView {
            id: linesView
            SplitView.fillWidth: true
            delegate: Text {
                text: nick + ": " + message
            }
        }
        ListView {
            id: chattersView
            visible: isPublic
            SplitView.preferredWidth: 100
            SplitView.maximumWidth: 300
            delegate: Text {
                text: nick
                MouseArea {
                    id: chatterMouseArea
                    anchors.fill: parent
                    onDoubleClicked: {
                        fafChat.join_private_channel(nick, channel_name)
                    }
                }
            }
        }
    }
}
