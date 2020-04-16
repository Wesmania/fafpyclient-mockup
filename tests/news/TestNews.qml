import QtQuick 2.4
import QtQuick.Controls 2.13
import "../../res/ui/news_tab"
import "../../res/ui/main_window"

ToplevelWindowTempl {
	News {
		anchors.fill: parent
	}

    Component.onCompleted: {
    	news.fetch()
    }
}
