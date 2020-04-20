from rx.subject import BehaviorSubject


class ModelItem:
    def __init__(self):
        self._data_fields = []

    def _add_obs(self, name, default=None):
        obsname = f"obs_{name}"

        def getobs(self):
            return getattr(self.obsname).value

        setattr(self, obsname, BehaviorSubject(default))
        setattr(self, name, property(getobs))
        self._data_fields.add(name)

    def field_dict(self):
        return {v: getattr(self, v) for v in self._data_fields}

    def update(self, vals):
        for f in self._data_fields:
            if f in vals:
                getattr(self, f"obs_{f}").on_next(f)

    def complete(self):
        """
        Completes observables so we can do fancy things like merge_all.
        """
        for f in self._data_fields:
            getattr(self, f"obs_{f}").on_completed()

    def id_key(self):
        raise NotImplementedError

    def __hash__(self):
        return hash(self.id_key())

    def __eq__(self, other):
        if type(self) is not type(other):
            return False
        return self.id_key == other.id_key
