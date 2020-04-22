import QtQuick 2.4

GridView {
    id: gameListView
    property alias gameModel: gameListView.model

    cellWidth: 400
    cellHeight: 200
    clip: true
    delegate: GameGridItem {
        width: gameListView.cellWidth
        height: gameListView.cellHeight
    }
}
