from ..Serializer import Serializer
from .serialize import serialize
from .deserialize import deserialize

class Serializer_JSON(Serializer):
    def dump(self, obj, file):
        pass
    def dumps(self, obj):
        return serialize(obj)
    def load(self, file):
        pass
    def loads(self, string):
        return deserialize(string)