import QtQuick 2.4
import QtQuick.Controls 2.13
import QtQuick.Layouts 1.3
import QtWebView 1.14

SplitView {
    readonly property string html_template: '
<head>
<link href="https://fonts.googleapis.com/css?family=Yanone+Kaffeesatz" rel="stylesheet" type="text/css">
</head>
<body>
<h1>%1</h1>
<hr>
<div id="container">
%2
</div>
</body>
'

        property alias newsModel: newsList.model
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
            onCurrentItemChanged: {
                if (currentItem) {
                    newsMainView.loadHtml(html_template.arg(currentItem.title).arg(currentItem.body))
                }
            }

            delegate: Text {
                property string title: model.news_title
                property string body: model.news_body

                id: newsItem
                text: news_title
                anchors.left: parent.left
                anchors.right: parent.right
                MouseArea {
                    id: newsListMouseArea
                    anchors.fill: parent
                    onClicked: newsList.currentIndex = index
                }
            }
        }

        WebView {
            id: newsMainView
            SplitView.fillWidth: true
        }
}
