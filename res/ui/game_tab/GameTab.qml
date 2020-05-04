import QtQuick 2.4
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.13
import "../util"

Item {
    id: gameTab
    property var gameModel: faf__tabs__games__model

    RowLayout {
        id: gameListBar
        width: parent.width
        anchors.top: parent.top

        CheckBox {
            id: showPrivGamesBox
            text: qsTr("Show private games")
            checked: gameModel.private_games_visible
            onToggled: gameModel.private_games_visible = checked
        }

        CheckBox {
            id: showModGamesBox
            text: qsTr("Show modded games")
            checked: gameModel.modded_games_visible
            onToggled: gameModel.modded_games_visible = checked
        }

        ResizingComboBox {
            id: gameSortBox

            // FIXME - has to be synced with python enum. Easy fix.
            model: ListModel {
                ListElement { idx: 0; text: qsTr("Sort by lobby age")}
                ListElement { idx: 1; text: qsTr("Sort by player count")}
                ListElement { idx: 2; text: qsTr("Sort by max players")}
                ListElement { idx: 3; text: qsTr("Sort by average rating")}
                ListElement { idx: 4; text: qsTr("Sort by title")}
            }
            textRole: "text"
            onActivated: gameModel.set_sort_type(model.get(currentIndex).idx)
        }
        Item {
            Layout.fillWidth: true
        }
    }

    GridView {
        id: gameListView
        width: parent.width
        anchors.top: gameListBar.bottom
        anchors.bottom: parent.bottom

        model: gameModel
        cellWidth: 400
        cellHeight: 200
        clip: true
        delegate: GameGridItem {
            width: gameListView.cellWidth
            height: gameListView.cellHeight
        }
    }

}
