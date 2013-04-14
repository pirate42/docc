# coding=utf-8
import unittest

from mock import MagicMock

from api.region import Region
from api.credentials import Credentials
from api.service import Service


class TestRegion(unittest.TestCase):
    def test___init__(self):
        region = Region(3, "def")
        self.assertEquals(3, region.id)
        self.assertEquals("def", region.name)


    def test___repr__(self):
        region = Region(3, "def")
        self.assertEqual("<3: def>", region.__repr__())

    def test___str__(self):
        region = Region(3, "def")
        self.assertEqual("3: def", region.__str__())

    def test_get(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'regions': [
                {'name': 'Region 1', 'id': 1},
                {'name': 'Region 2', 'id': 2},
            ]
        }
        service.get = MagicMock(return_value=response)
        region = Region.get(service, 1)
        self.assertEquals(region.id, 1)
        self.assertEquals(region.name, 'Region 1')


    def test_regions(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'regions': [
                {'name': 'Region 1', 'id': 1},
                {'name': 'Region 2', 'id': 2},
            ]
        }
        service.get = MagicMock(return_value=response)
        regions = Region.regions(service)
        self.assertEquals(len(regions), 2)


    def test___eq__(self):
        region1 = Region(1, "USA")
        region2 = Region(1, "USA")
        region3 = Region(2, "USA")
        region4 = Region(1, "NL")
        self.assertTrue(region1.__eq__(region2))
        self.assertTrue(region2.__eq__(region1))
        self.assertFalse(region1.__eq__(region3))
        self.assertFalse(region1.__eq__(region4))

    def test___ne__(self):
        region1 = Region(1, "USA")
        region2 = Region(1, "USA")
        region3 = Region(2, "USA")
        region4 = Region(1, "NL")
        self.assertFalse(region1.__ne__(region2))
        self.assertFalse(region2.__ne__(region1))
        self.assertTrue(region1.__ne__(region3))
        self.assertTrue(region1.__ne__(region4))


if __name__ == '__main__':
    unittest.main()
