# coding=utf-8
import unittest

from mock import MagicMock, patch

from docc.droplet import Droplet, Status
from docc.service import Service
from docc.credentials import Credentials
from docc.size import Size
from docc.image import Image
from docc.region import Region


class TestDroplet(unittest.TestCase):
    def test___init__(self):
        droplet = Droplet(
            Status.NEW,
            21345,
            "This is a test",
            Size(1, "512M"),
            Image(34, "Ubuntu 10.02", "A linux distribution"),
            "1.2.3.4",
            Region(1, "USA"),
            False,
        )
        self.assertEqual(droplet.status, Status.NEW)
        self.assertEqual(droplet.id, 21345)
        self.assertEqual(droplet.name, "This is a test")
        self.assertEqual(droplet.size, Size(1, "512M"))
        self.assertEqual(droplet.image,
                         Image(34, "Ubuntu 10.02", "A linux distribution"))
        self.assertEqual(droplet.region, Region(1, "USA"))
        self.assertEqual(droplet.ip_address, "1.2.3.4")
        self.assertFalse(droplet.backups)

    def test___repr__(self):
        droplet = Droplet(
            Status.NEW,
            21345,
            "This is a test",
            Size(1, "512M"),
            Image(34, "Ubuntu 10.02", "A linux distribution"),
            "1.2.3.4",
            Region(1, "USA"),
            False,
        )
        self.assertEqual("<21345: This is a test, new, 1.2.3.4>",
                         droplet.__repr__())

    def test___str__(self):
        droplet = Droplet(
            Status.NEW,
            21345,
            "This is a test",
            Size(1, "512M"),
            Image(34, "Ubuntu 10.02", "A linux distribution"),
            "1.2.3.4",
            Region(1, "USA"),
            False,
        )
        self.assertEqual("21345: This is a test, new, 1.2.3.4, 512M",
                         droplet.__str__())

    def test_droplets(self):
        size_patcher = patch(
            'docc.size.Size.get',
            new=MagicMock(return_value=Size(66, "512M"))
        )
        size_patcher.start()

        image_patcher = patch(
            'docc.image.Image.get',
            MagicMock(
                return_value=Image(25306, "Ubuntu 1", "Ubuntu Description")
            )
        )
        image_patcher.start()

        region_patcher = patch(
            'docc.region.Region.get',
            MagicMock(return_value=Region(1, "USA"))
        )
        region_patcher.start()

        def teardown():
            size_patcher.stop()
            region_patcher.stop()
            image_patcher.stop()

        self.addCleanup(teardown)

        service_response = {
            "status": "OK",
            "droplets": [
                {
                    "id": 151220,
                    "name": "cloud.segonds.org",
                    "image_id": 25306,
                    "size_id": 66,
                    "region_id": 1,
                    "backups_active": None,
                    "ip_address": "208.68.38.181",
                    "status": "new"
                },
                {
                    "id": 151221,
                    "name": "cloud2.segonds.org",
                    "image_id": 25306,
                    "size_id": 66,
                    "region_id": 1,
                    "backups_active": None,
                    "ip_address": "208.68.38.182",
                    "status": "new"
                },
            ]
        }
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        service.get = MagicMock(return_value=service_response)

        droplets = Droplet.droplets(service)

        self.assertEquals(len(droplets), 2)
        droplet = droplets[0]
        self.assertEquals(droplet.id, 151220)
        self.assertEquals(droplet.name, "cloud.segonds.org")
        self.assertEquals(droplet.size, Size(66, "512M"))
        self.assertEquals(droplet.status, Status.NEW)

    def test_get(self):
        size_patcher = patch(
            'docc.size.Size.get',
            new=MagicMock(return_value=Size(66, "512M"))
        )
        size_patcher.start()

        image_patcher = patch(
            'docc.image.Image.get',
            MagicMock(
                return_value=Image(25306, "Ubuntu 1", "Ubuntu Description")
            )
        )
        image_patcher.start()

        region_patcher = patch(
            'docc.region.Region.get',
            MagicMock(return_value=Region(1, "USA"))
        )
        region_patcher.start()

        def teardown():
            size_patcher.stop()
            region_patcher.stop()
            image_patcher.stop()

        self.addCleanup(teardown)

        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            "status": "OK",
            "droplet": {
                "id": 151220,
                "name": "cloud.segonds.org",
                "image_id": 25306,
                "size_id": 66,
                "region_id": 1,
                "backups_active": None,
                "ip_address": "208.68.38.181",
                "status": "active"
            }
        }

        mock = MagicMock(return_value=response)
        service.get = mock
        droplet = Droplet.get(service, 151220)
        self.assertEquals(droplet.id, 151220)
        self.assertEquals(droplet.name, "cloud.segonds.org")
        self.assertEquals(droplet.size, Size(66, "512M"))
        self.assertEquals(droplet.status, Status.ACTIVE)

    def test_shutdown(self):
        droplet = Droplet(
            Status.NEW,
            21345,
            "This is a test",
            Size(1, "512M"),
            Image(34, "Ubuntu 10.02", "A linux distribution"),
            "1.2.3.4",
            Region(1, "USA"),
            False,
        )
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            "status": "OK",
            "event_id": 1417387
        }
        mock = MagicMock(return_value=response)
        service.get = mock
        self.assertTrue(droplet.shutdown(service))
        mock.assert_called_once_with(
            'droplets/21345/shutdown'
        )

    def test_reboot(self):
        droplet = Droplet(
            Status.NEW,
            21345,
            "This is a test",
            Size(1, "512M"),
            Image(34, "Ubuntu 10.02", "A linux distribution"),
            "1.2.3.4",
            Region(1, "USA"),
            False,
        )
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            "status": "OK",
            "event_id": 1417387
        }
        mock = MagicMock(return_value=response)
        service.get = mock
        self.assertTrue(droplet.reboot(service))
        mock.assert_called_once_with(
            'droplets/21345/reboot'
        )

    def test_power_cycle(self):
        droplet = Droplet(
            Status.NEW,
            21345,
            "This is a test",
            Size(1, "512M"),
            Image(34, "Ubuntu 10.02", "A linux distribution"),
            "1.2.3.4",
            Region(1, "USA"),
            False,
        )
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            "status": "OK",
            "event_id": 1417387
        }
        mock = MagicMock(return_value=response)
        service.get = mock
        self.assertTrue(droplet.power_cycle(service))
        mock.assert_called_once_with(
            'droplets/21345/power_cycle'
        )

    def test_power_off(self):
        droplet = Droplet(
            Status.ACTIVE,
            21345,
            "This is a test",
            Size(1, "512M"),
            Image(34, "Ubuntu 10.02", "A linux distribution"),
            "1.2.3.4",
            Region(1, "USA"),
            False,
        )
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            "status": "OK",
            "event_id": 1417387
        }
        mock = MagicMock(return_value=response)
        service.get = mock
        self.assertTrue(droplet.power_off(service))
        mock.assert_called_once_with(
            'droplets/21345/power_off'
        )

    def test_power_on(self):
        droplet = Droplet(
            Status.OFF,
            21345,
            "This is a test",
            Size(1, "512M"),
            Image(34, "Ubuntu 10.02", "A linux distribution"),
            "1.2.3.4",
            Region(1, "USA"),
            False,
        )
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            "status": "OK",
            "event_id": 1417387
        }
        mock = MagicMock(return_value=response)
        service.get = mock
        self.assertTrue(droplet.power_on(service))
        mock.assert_called_once_with(
            'droplets/21345/power_on'
        )

    def test_destroy(self):
        droplet = Droplet(
            Status.OFF,
            21345,
            "This is a test",
            Size(1, "512M"),
            Image(34, "Ubuntu 10.02", "A linux distribution"),
            "1.2.3.4",
            Region(1, "USA"),
            False,
        )
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            "status": "OK",
            "event_id": 1417387
        }
        mock = MagicMock(return_value=response)
        service.get = mock
        self.assertTrue(droplet.destroy(service))
        mock.assert_called_once_with(
            'droplets/21345/destroy'
        )


if __name__ == '__main__':
    unittest.main()