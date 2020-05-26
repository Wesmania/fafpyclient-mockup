from collections.abc import MutableMapping
from itertools import chain
from functools import reduce
import yaml


class Path(yaml.YAMLObject):
    yaml_tag = '!Path'

    def __init__(self, env, path_fmt):
        self._path_fmt = path_fmt
        self.path = path_fmt.format(ROOT_PATH=env.ROOT_PATH)

    @classmethod
    def from_yaml(cls, env):
        return lambda loader, node: cls(env, node.value)

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_scalar(cls.yaml_tag, data.path_fmt)


class ConfigDict(MutableMapping):
    """
    Allows access to 2 dicts - default config and user config. Returns subdicts
    as instances of ConfigDict.
    User config is always contained in default config.
    """
    def __init__(self, parent, deft_config, user_config):
        MutableMapping.__init__(self)
        self._parent = parent
        self._deft_config = deft_config
        self._user_config = user_config

    def __len__(self):
        return len(self._deft_config) + len(self._user_config)

    def __iter__(self):
        return chain(iter(self._deft_config), iter(self._user_config))

    def __getitem__(self, key):
        deft_val = self._deft_config[key]
        if isinstance(deft_val, dict):
            user_val = self._user_config.setdefault(key, {})
            return ConfigDict(self._parent, deft_val, user_val)
        else:
            if key in self._user_config:
                return self._user_config[key]
            else:
                return deft_val

    def __setitem__(self, key, value):
        self._user_config[key] = value

    def __delitem__(self, key):
        del self._user_config[key]

    def save(self):
        self._parent.save()


def deepmerge(main, extra):
    for key in extra:
        if key in main and isinstance(main[key], dict):
            deepmerge(main[key], extra[key])
        else:
            main[key] = extra[key]
    return main


class Config(ConfigDict):
    def __init__(self, environment, default_configs, user_config):

        class Loader(yaml.SafeLoader):
            pass

        class Dumper(yaml.SafeDumper):
            pass

        Loader.add_constructor('!Path', Path.from_yaml(environment))
        Dumper.add_multi_representer('!Path', Path.to_yaml)

        self._loader = Loader
        self._dumper = Dumper

        self._user_config_file = user_config
        configs = [yaml.load(open(f, "r").read(), Loader=self._loader)
                   for f in default_configs]
        deft_config = reduce(deepmerge, configs, {})
        try:
            app_config = yaml.load(open(user_config, "r").read(),
                                   Loader=self._loader)
        except Exception:   # TODO log
            app_config = {}

        ConfigDict.__init__(self, None, deft_config, app_config)

    def save(self):
        self._remove_empty_keys(self._user_config)
        open(self._user_config_file, "w").write(yaml.dump(self._user_config,
                                                          Dumper=self._dumper))

    def _remove_empty_keys(self, d):
        to_remove = []
        for k, v in d.items():
            if isinstance(v, dict):
                self._remove_empty_keys(v)
                if not v:
                    to_remove.append(k)
        for k in to_remove:
            del d[k]
