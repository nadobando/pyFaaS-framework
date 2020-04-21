class CaseInsensitiveDict(dict):
    def __contains__(self, key):
        return dict.__contains__(self, key.lower())

    def __getitem__(self, key):
        return dict.__getitem__(self, key.lower())['val']

    def __setitem__(self, key, value):
        return dict.__setitem__(self, key.lower(), {'key': key, 'val': value})

    def get(self, key, default=None):
        try:
            v = dict.__getitem__(self, key.lower())
        except KeyError:
            return default
        else:
            return v['val']

    def __delitem__(self, key):
        del self.__dict__[key.lower()]

    def __iter__(self):
        return (casedkey for casedkey, mappedvalue in self.values())

    def items(self):
        return [(v['key'], v['val']) for v in dict.values(self)]

    def keys(self):
        return [v['key'] for v in dict.values(self)]

    def values(self):
        return [v['val'] for v in dict.values(self)]
