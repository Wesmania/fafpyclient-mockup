import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3

Item {
    property string channelName;
    property bool isPublic;
    property string channelTopic;
    property alias channelLinesModel : channelLinesView.model
    property alias channelChattersModel : channelChattersView.model

    TextArea {
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
            id: channelLinesView
            SplitView.fillWidth: true
            delegate: Text {
                text: nick + ": " + message
            }
        }
        ListView {
            id: channelChattersView
            SplitView.preferredWidth: 100
            SplitView.maximumWidth: 300
            delegate: Text {
                text: nick
            }
        }
    }
}
