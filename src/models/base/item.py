from rx.subject import BehaviorSubject
from rx import operators as ops


class ModelItem:
    def __init__(self):
        self._data_fields = []

    def _add_obs(self, name, default=None):
        subject = BehaviorSubject(default)
        uniq_subject = subject.pipe(
            ops.distinct_until_changed()
        )

        def getobs(self):
            return getattr(self, f"_obs_{name}").value

        def setobs(self, v):
            getattr(self, f"_obs_{name}").on_next(v)

        setattr(self, f"_obs_{name}", subject)
        setattr(self, f"obs_{name}", uniq_subject)
        setattr(self.__class__, name, property(getobs, setobs))
        self._data_fields.append(name)

    def field_dict(self):
        return {v: getattr(self, v) for v in self._data_fields}

    def update(self, vals):
        for f in self._data_fields:
            if f in vals:
                setattr(self, f, vals[f])

    def complete(self):
        """
        Completes observables so we can do fancy things like merge_all.
        """
        for f in self._data_fields:
            getattr(self, f"_obs_{f}").on_completed()

    @property
    def id_key(self):
        raise NotImplementedError

    def __hash__(self):
        return hash(self.id_key)

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.id_key == other.id_key
