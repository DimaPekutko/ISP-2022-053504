from .create_serializer import create_serializer
from .serializer_table import SERIALIZERS

def func():
    return 3 + 2

val = func()

class Some:
    b = 228
    def render(self, a):
        self.b=a*val
