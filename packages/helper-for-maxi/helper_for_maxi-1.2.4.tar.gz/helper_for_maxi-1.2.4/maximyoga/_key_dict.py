class kdict(dict):
    r"""Like a dict but accessible with x.key and x["key"]"""

    def __getattr__(self, name: str):
        return self[name]

    def __setattr__(self, name, value) -> None:
        self[name] = value

    def __delattr__(self, name) -> None:
        del self[name]

    def convert_inner_dicts(self, recursive: bool = False) -> None:
        for k, v in self.items():
            if isinstance(v, dict) and not isinstance(v, kdict):
                self[k] = kdict(v)
                if recursive:
                    self[k].convert_inner_dicts(True)