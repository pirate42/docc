# coding=utf-8
import unittest

from mock import MagicMock

from docc.api.sshkey import SSHKey
from docc.api.credentials import Credentials
from docc.api.service import Service


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
        self.assertIsNone(key.public_key)

        key = SSHKey(4, "abc", "def")
        self.assertEquals(4, key.id)
        self.assertEquals("abc", key.name)
        self.assertEquals("def", key.public_key)

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


if __name__ == '__main__':
    unittest.main()
