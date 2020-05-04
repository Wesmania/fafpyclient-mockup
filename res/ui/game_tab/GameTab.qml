import QtQuick 2.4

GridView {
    property alias gameModel: gameListView.model

    gameModel: faf__tabs__games__model
    cellWidth: 400
    cellHeight: 200
    clip: true
    delegate: GameGridItem {
        width: gameListView.cellWidth
        height: gameListView.cellHeight
    }
}
