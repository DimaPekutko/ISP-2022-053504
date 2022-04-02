import module_test

def test_func() -> int:
    return 228


class TestClass():
    some_bool_value = True
    class_value = 18
    c = 10.2

    def __init__(self, a: int, b: int = 2):
        self.c += (a+b)

    def count(self) -> int:
        return self.c/18

class Test():
    c = 1000
    def count(self) -> int:
        return self.c/18


def func_with_external_logic():
    return module_test.external_module_logic()*100


test_obj = Test()