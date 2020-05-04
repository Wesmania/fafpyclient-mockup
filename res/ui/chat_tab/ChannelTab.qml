import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3

Item {
    Text {
        id: chatTopic
        width: parent.width
        anchors.top: parent.top
        text: channel_topic
    }

    SplitView {
        width: parent.width
        anchors.top: chatTopic.bottom
        anchors.bottom: parent.bottom
        ListView {
            id: linesView
            model: lines_model
            SplitView.fillWidth: true
            delegate: Text {
                text: nick + ": " + message
            }
        }
        ListView {
            id: chattersView
            model: chatters_model
            visible: is_public
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
