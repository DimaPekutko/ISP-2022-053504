import unittest
import pekutko_serializer as lib

import data

json_ser = lib.JsonSerializer()


class TestJson(unittest.TestCase):
    def test_func(self):
        self.assertEqual(
            data.test_func(),
            json_ser.loads(json_ser.dumps(data.test_func))()
        )

    def test_class(self):
        arg = 12
        obj1 = data.TestClass(arg, arg)
        obj2 = json_ser.loads(json_ser.dumps(data.TestClass))(arg, arg)
        self.assertEqual(obj1.count(), obj2.count())
    
    def test_obj(self):
        obj = data.test_obj
        obj.c = 22
        self.assertEqual(
            obj.count(), 
            json_ser.loads(json_ser.dumps(obj)).count()
        )
    
    def test_module(self):
        func = data.func_with_external_logic
        self.assertEqual(
            func(),
            json_ser.loads(json_ser.dumps(func))()
        )


if __name__ == '__main__':
    unittest.main()  # pragma: no cover
