import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3
import QtWebView 1.14

SplitView {
        property alias newsModel: newsList.model
        property alias newsMainView: newsMainView
        property alias newsList: newsList
        property alias newsListMouseArea: newsListMouseArea

        orientation: Qt.Horizontal
        ListView {
            id: newsList
            SplitView.minimumWidth: 100
            SplitView.preferredWidth: 200
            SplitView.maximumWidth: 300

            focus: true
            highlight: Rectangle {
                color: "lightsteelblue"; radius: 5
            }
            highlightFollowsCurrentItem: true

            MouseArea {
                id: newsListMouseArea
                anchors.fill: parent
            }

            delegate: Text {
                id: newsItem
                text: display['title']
                anchors.left: parent.left
                anchors.right: parent.right

            }
        }

        WebView {
            id: newsMainView
            SplitView.fillWidth: true
        }
}
