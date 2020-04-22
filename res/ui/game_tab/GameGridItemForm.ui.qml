import QtQuick 2.4

Item {
    Rectangle {
        color: "#333948"
        anchors.fill: parent
        anchors.margins: 6
        Image {
            id: gameMap
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            source: ROOT_PATH + "/res/icons/games/unknown_map.png"
            height: parent.height
            width: parent.height
            fillMode: Image.PreserveAspectFit
        }

        Text {
            id: gameTitle
            anchors.top: parent.top
            anchors.left: gameMap.right
            anchors.right: parent.right
            text: title
            font.pointSize: 12
        }

        Text {
            id: gameMod
            anchors.top: gameTitle.bottom
            anchors.left: gameMap.right
            anchors.right: parent.right
            text: mod
            font.pointSize: 10
        }

        Text {
            id: gamePlayers
            anchors.top: gameMod.bottom
            anchors.left: gameMap.right
            text: players
            font.pointSize: 12
        }

        Text {
            id: gameAvgRating
            anchors.top: gameMod.bottom
            anchors.right: parent.right
            text: avg_rating
            font.pointSize: 12
        }

        Text {
            id: gameHost
            anchors.top: gamePlayers.bottom
            anchors.left: gameMap.right
            anchors.right: parent.right
            text: host
            font.pointSize: 12
        }
    }
}

/*##^##
Designer {
    D{i:0;autoSize:true;height:480;width:640}
}
##^##*/
