import copy
import unittest
from wiki.web.user import *


class TestUserManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.um = UserManager(os.getcwd())

        cls.data = {
            'user1': {
                'active': True,
                'roles': [],
                'authentication_method': "hash",
                'authenticated': False,
                'hash': make_salted_hash("pass1")
            },
            'user2': {
                'active': False,
                'roles': [],
                'authentication_method': "cleartext",
                'authenticated': False,
                'password': "pass2"
            }
        }

        f = open(cls.um.file, 'w')
        f.write(json.dumps(cls.data, indent=2))
        f.close()

    def test_read(self):
        data = self.um.read()
        self.assertTrue("user1" in data and "user2" in data and data['user1']['authentication_method'] == "hash"
                        and data['user1']['authentication_method'] == "hash")

    def test_write(self):
        um = UserManager(os.getcwd() + "/test")
        data = copy.deepcopy(self.data)
        data["user3"] = {
            'active': False,
            'roles': [],
            'authentication_method': "hash",
            'authenticated': False
        }
        um.write(data)
        data = um.read()
        success = "user3" in data and data['user3']['authentication_method'] == "hash"
        os.remove(um.file)
        self.assertTrue(success)

    def test_add_user(self):
        self.um.add_user("user3", "pass3", authentication_method="cleartext")
        data = self.um.read()
        success = "user3" in data and data['user3']['password'] == "pass3"
        self.um.write(self.data)
        self.assertTrue(success)

    def test_get_user(self):
        user = self.um.get_user("user2")
        self.assertTrue(user is not None and user.data['password'] == "pass2")

    def test_delete_user(self):
        um = UserManager(os.getcwd() + "/test")
        um.write(self.data)
        um.delete_user("user1")
        success = "user1" not in um.read()
        os.remove(um.file)
        self.assertTrue(success)

    def test_update(self):
        self.um.update("user2", {
            'active': True,
            'roles': [],
            'authentication_method': "cleartext",
            'authenticated': False,
            'password': "pass2"
        })
        data = self.um.read()
        success = data['user3']['active']
        self.um.update("user2", {
            'active': False,
            'roles': [],
            'authentication_method': "cleartext",
            'authenticated': False,
            'password': "pass2"
        })
        self.assertTrue(success)

    @classmethod
    def tearDownClass(cls):
        os.remove(os.path.join(os.getcwd(), "users.json"))


class TestUser(unittest.TestCase):

    def test_check_password(self):
        user1 = User(None, "user1", {
            'active': True,
            'roles': [],
            'authentication_method': "hash",
            'authenticated': False,
            'hash': make_salted_hash("pass1")
        })

        user2 = User(None, "user2", {
            'active': True,
            'roles': [],
            'authentication_method': "cleartext",
            'authenticated': False,
            'password': "pass2"
        })
        self.assertTrue(user1.check_password("pass1") and user2.check_password("pass2"))


if __name__ == '__main__':
    unittest.main()
