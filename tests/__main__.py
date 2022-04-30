import unittest

import luogu


class TestUser(unittest.TestCase):
    def test_404(self):
        self.assertRaisesRegex(
            luogu.NotFoundHttpException, r"^用户未找到$", luogu.User, 0
        )

    def test_kkksc03(self):
        u = luogu.User(1)
        self.assertIsInstance(u.prize, list)
        self.assertEqual(u.uid, 1)
        self.assertEqual(u.name, "kkksc03")
        self.assertEqual(u.is_admin, True)
        self.assertEqual(u.is_root, True)

    def test_wangxinhe(self):
        u = luogu.User(108135)
        self.assertIsInstance(u.prize, list)
        self.assertEqual(u.uid, 108135)
        self.assertEqual(u.name, "wangxinhe")
        self.assertEqual(u.is_admin, False)
        self.assertIs(u.is_root, None)


if __name__ == "__main__":
    unittest.main()
