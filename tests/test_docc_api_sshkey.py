# coding=utf-8
import unittest

from mock import MagicMock, call

from docc.sshkey import SSHKey
from docc.credentials import Credentials
from docc.service import Service


class TestSSHKey(unittest.TestCase):
    def test___eq__(self):
        key1 = SSHKey(1, "My Key", "A linux distribution")
        key2 = SSHKey(1, "My Key", "A linux distribution")
        key3 = SSHKey(2, "My Key", "A linux distribution")
        key4 = SSHKey(1, "My Key 2", "A linux distribution")
        key5 = SSHKey(1, "My Key", "A windows distribution")
        key6 = SSHKey(1, "My Key")
        key7 = SSHKey(1, "My Key")
        self.assertTrue(key1.__eq__(key2))
        self.assertTrue(key2.__eq__(key1))
        self.assertFalse(key1.__eq__(key3))
        self.assertFalse(key1.__eq__(key4))
        self.assertFalse(key1.__eq__(key5))
        self.assertTrue(key6.__eq__(key7))

    def test___init__(self):
        key = SSHKey(3, "def")
        self.assertEquals(3, key.id)
        self.assertEquals("def", key.name)
        self.assertIsNone(key.public)

        key = SSHKey(4, "abc", "def")
        self.assertEquals(4, key.id)
        self.assertEquals("abc", key.name)
        self.assertEquals("def", key.public)

    def test___ne__(self):
        key1 = SSHKey(1, "My Key", "A linux distribution")
        key2 = SSHKey(1, "My Key", "A linux distribution")
        key3 = SSHKey(2, "My Key", "A linux distribution")
        key4 = SSHKey(1, "My Key 2", "A linux distribution")
        key5 = SSHKey(1, "My Key", "A windows distribution")
        key6 = SSHKey(1, "My Key")
        key7 = SSHKey(1, "My Key")
        self.assertFalse(key1.__ne__(key2))
        self.assertFalse(key2.__ne__(key1))
        self.assertTrue(key1.__ne__(key3))
        self.assertTrue(key1.__ne__(key4))
        self.assertTrue(key1.__ne__(key5))
        self.assertFalse(key6.__ne__(key7))

    def test___repr__(self):
        key = SSHKey(3, "def")
        self.assertEqual("<3: def>", key.__repr__())

    def test___str__(self):
        key = SSHKey(3, "def")
        self.assertEqual("3: def", key.__str__())

    def test_keys(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'ssh_keys': [
                {'name': 'My Key 1', 'id': 1},
                {'name': 'My Key 2', 'id': 2},
            ]
        }
        service.get = MagicMock(return_value=response)
        keys = SSHKey.keys(service)
        self.assertEquals(len(keys), 2)


    def test_destroy(self):
        key = SSHKey(
            21345,
            "This is a test",
        )
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            "status": "OK",
            "event_id": 1417387
        }
        mock = MagicMock(return_value=response)
        service.get = mock
        self.assertTrue(key.destroy(service))
        mock.assert_called_once_with(
            'ssh_keys/21345/destroy'
        )

    def test_get(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'ssh_key': {
                'name': 'Name 1',
                'id': 1,
                'ssh_pub_key': "asr2354tegrh23425erfwerwerffghrgh3455"
            },
        }

        service.get = MagicMock(return_value=response)
        key = SSHKey.get(service, 1)
        self.assertEquals(key.id, 1)
        self.assertEquals(key.name, 'Name 1')
        self.assertEquals(key.public, "asr2354tegrh23425erfwerwerffghrgh3455")


    def test_create(self):
        credentials = Credentials("abc", "def")
        service = Service(credentials)
        response = {
            'status': 'OK',
            'ssh_key': {
                'name': 'Name 1',
                'id': 1,
                'ssh_pub_key': "asr2354tegrh23425erfwerwerffghrgh3455"
            },
        }

        mock = MagicMock(return_value=response)
        service.get = mock
        key = SSHKey.create(
            service,
            "Name 1",
            "asr2354tegrh23425erfwerwerffghrgh3455"
        )
        self.assertEquals(key.id, 1)
        self.assertEquals(key.name, 'Name 1')
        self.assertEquals(key.public, "asr2354tegrh23425erfwerwerffghrgh3455")
        mock.assert_has_calls(
            [
                call(
                    'ssh_keys/new',
                    {
                        "name": "Name 1",
                        "ssh_pub_key": "asr2354tegrh23425erfwerwerffghrgh3455"
                    })
            ]
        )

    def test_details(self):
        key = SSHKey(1, "toto", "ssh-rsa dfwerwe324fsdf toto@example.com")
        expected = "Id: 1\nName: toto\n" \
                   "Public key: ssh-rsa dfwerwe324fsdf toto@example.com"
        self.assertEquals(key.details(), expected)


if __name__ == '__main__':
    unittest.main()
