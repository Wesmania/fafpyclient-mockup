import QtQuick 2.4

NewsForm {
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
    newsModel: faf__tabs__news__model
    newsList.onCurrentIndexChanged: {
        var idx = newsList.currentIndex
        var contents = newsModel.news_contents(idx)
        newsMainView.loadHtml(html_template.arg(contents['title']).arg(contents['body']))
    }

    newsListMouseArea.onClicked: {
        var x = newsListMouseArea.mouseX
        var y = newsListMouseArea.mouseY
        var idx = newsList.indexAt(x, y)
        if (idx !== -1)
            newsList.currentIndex = idx
    }
}
