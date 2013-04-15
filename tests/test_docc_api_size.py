# coding=utf-8
import unittest
from mock import MagicMock
from docc.service import Service
from docc.size import Size
from docc.credentials import Credentials


class TestSize(unittest.TestCase):
    def test___init__(self):
        size = Size(3, "def")
        self.assertEquals(3, size.id)
        self.assertEquals("def", size.name)

    def test_get(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'sizes': [
                {'name': '256M', 'id': 1},
                {'name': '512M', 'id': 2},
            ]
        }
        service.get = MagicMock(return_value=response)
        size = Size.get(service, 1)
        self.assertEquals(size.id, 1)
        self.assertEquals(size.name, '256M')

    def test_sizes(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'sizes': [
                {'name': '256M', 'id': 1},
                {'name': '512M', 'id': 2},
            ]
        }
        service.get = MagicMock(return_value=response)
        sizes = Size.sizes(service)
        self.assertEquals(len(sizes), 2)


    def test___eq__(self):
        size1 = Size(1, "512M")
        size2 = Size(1, "512M")
        size3 = Size(2, "512M")
        size4 = Size(1, "1024M")
        self.assertTrue(size1.__eq__(size2))
        self.assertTrue(size2.__eq__(size1))
        self.assertFalse(size1.__eq__(size3))
        self.assertFalse(size1.__eq__(size4))


    def test___ne__(self):
        size1 = Size(1, "512M")
        size2 = Size(1, "512M")
        size3 = Size(2, "512M")
        size4 = Size(1, "1024M")
        self.assertFalse(size1.__ne__(size2))
        self.assertFalse(size2.__ne__(size1))
        self.assertTrue(size1.__ne__(size3))
        self.assertTrue(size1.__ne__(size4))


    def test___repr__(self):
        size = Size(3, "def")
        self.assertEqual("<3: def>", size.__repr__())


    def test___str__(self):
        size = Size(3, "def")
        self.assertEqual("3: def", size.__str__())


if __name__ == '__main__':
    unittest.main()
