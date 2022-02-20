from .serializer_table import SERIALIZERS
from .Serializer.Serializer import Serializer

def create_serializer(ser_name: str) -> Serializer:
    for ser_name, ser_type in SERIALIZERS.items():
        if ser_name.lower() == ser_name:
            return ser_type()