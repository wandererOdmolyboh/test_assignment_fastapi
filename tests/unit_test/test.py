import unittest
from src.auth.utils import hash_password


class TestHashPassword(unittest.TestCase):
    def test_hash_password(self):
        password = "testpassword"
        hashed_password = hash_password(password)
        self.assertNotEqual(password, hashed_password)
        self.assertTrue(hashed_password.startswith("$2b$"))


if __name__ == '__main__':
    unittest.main()
