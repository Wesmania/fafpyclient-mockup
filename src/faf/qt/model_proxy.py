from rx import operators as ops

from faf.qt.model import QtDictListModel


class InternalModelQtProxy(QtDictListModel):
    def __init__(self, item_set):
        QtDictListModel.__init__(self)
        self._item_set = item_set

        item_set.added.subscribe(self._add_item)
        item_set.removed.subscribe(self._remove_item)
        item_set.cleared.subscribe(self._clear_items)

    def _add_item(self, item):
        self._add(item.id_key, item)

    def _remove_item(self, item):
        self._remove(item.id_key)

    def _clear_items(self, _):
        self._clear()

    def _update_stream(self, stream_selector):

        def select(item):
            return stream_selector(item).pipe(
                ops.map(lambda _: item)
            )

        return self._item_set.added.pipe(
            ops.map(select),
            ops.merge_all()
        )

    def _update_roles_at(self, stream_selector, role):
        self._update_stream(stream_selector).subscribe(
            lambda g: self._update(g, role.value))
