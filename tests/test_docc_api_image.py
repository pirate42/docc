# coding=utf-8
import unittest

from mock import MagicMock

from docc.image import Image
from docc.credentials import Credentials
from docc.service import Service


class TestImage(unittest.TestCase):
    def test___init__(self):
        image = Image(3, "def", "abc")
        self.assertEquals(3, image.id)
        self.assertEquals("def", image.name)
        self.assertEquals("abc", image.distribution)

    def test___repr__(self):
        region = Image(3, "def", "abc")
        self.assertEqual("<3: def>", region.__repr__())

    def test___str__(self):
        region = Image(3, "def", "abc")
        self.assertEqual("3: def, abc", region.__str__())

    def test_get(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'image': {'name': 'Name 1',
                      'id': 1,
                      'distribution': "Ubuntu 10.04"
            },
        }

        service.get = MagicMock(return_value=response)
        image = Image.get(service, 1)
        self.assertEquals(image.id, 1)
        self.assertEquals(image.name, 'Name 1')

    def test_images(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'images': [
                {'name': 'Name 1',
                 'id': 1,
                 'distribution': "Ubuntu 10.04"
                },
                {'name': 'Name 2',
                 'id': 2,
                 'distribution': "Ubuntu 12.04"
                },
            ]
        }

        mock = MagicMock(return_value=response)
        service.get = mock
        images = Image.images(service)
        mock.assert_called_once_with('images')
        self.assertEquals(len(images), 2)


    def test_global_images(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'images': [
                {'name': 'Name 1',
                 'id': 1,
                 'distribution': "Ubuntu 10.04"
                },
                {'name': 'Name 2',
                 'id': 2,
                 'distribution': "Ubuntu 12.04"
                },
            ]
        }

        mock = MagicMock(return_value=response)
        service.get = mock
        images = Image.global_images(service)
        mock.assert_called_once_with('images', {'filter': 'global'})
        self.assertEquals(len(images), 2)

    def test_my_images(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'images': [
                {'name': 'Name 1',
                 'id': 1,
                 'distribution': "Ubuntu 10.04"
                },
                {'name': 'Name 2',
                 'id': 2,
                 'distribution': "Ubuntu 12.04"
                },
            ]
        }

        mock = MagicMock(return_value=response)
        service.get = mock
        images = Image.my_images(service)
        mock.assert_called_once_with('images', {'filter': 'my_images'})
        self.assertEquals(len(images), 2)

    def test___eq__(self):
        image1 = Image(1, "Ubuntu 10.02", "A linux distribution")
        image2 = Image(1, "Ubuntu 10.02", "A linux distribution")
        image3 = Image(2, "Ubuntu 10.02", "A linux distribution")
        image4 = Image(1, "Ubuntu 12.10", "A linux distribution")
        image5 = Image(1, "Ubuntu 10.02", "A windows distribution")
        self.assertTrue(image1.__eq__(image2))
        self.assertTrue(image2.__eq__(image1))
        self.assertFalse(image1.__eq__(image3))
        self.assertFalse(image1.__eq__(image4))
        self.assertFalse(image1.__eq__(image5))

    def test___ne__(self):
        image1 = Image(1, "Ubuntu 10.02", "A linux distribution")
        image2 = Image(1, "Ubuntu 10.02", "A linux distribution")
        image3 = Image(2, "Ubuntu 10.02", "A linux distribution")
        image4 = Image(1, "Ubuntu 12.10", "A linux distribution")
        image5 = Image(1, "Ubuntu 10.02", "A windows distribution")
        self.assertFalse(image1.__ne__(image2))
        self.assertFalse(image2.__ne__(image1))
        self.assertTrue(image1.__ne__(image3))
        self.assertTrue(image1.__ne__(image4))
        self.assertTrue(image1.__ne__(image5))


    def test_destroy(self):
        image = Image(
            21345,
            "This is a test",
            "This is a test"
        )
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            "status": "OK",
            "event_id": 1417387
        }
        mock = MagicMock(return_value=response)
        service.get = mock
        self.assertTrue(image.destroy(service))
        mock.assert_called_once_with(
            'images/21345/destroy'
        )


if __name__ == '__main__':
    unittest.main()
