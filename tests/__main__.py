import unittest

import luogu


class TestUser(unittest.TestCase):
    def test_404(self):
        self.assertRaisesRegex(
            luogu.NotFoundHttpException, r"^用户未找到$", luogu.User, 0
        )

    def test_equal(self):
        self.assertEqual(luogu.User(1), luogu.User(1))

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

    def test_problems(self):
        u = luogu.User(108135)
        passed_problems = u.passed_problems
        self.assertIsInstance(passed_problems[0], luogu.Problem)
        submitted_problems = u.submitted_problems
        self.assertIsInstance(submitted_problems[0], luogu.Problem)
        self.assertIsInstance(submitted_problems[0].provider, luogu.User)
        self.assertIsInstance(submitted_problems[0].provider, luogu.User)


class TestProblem(unittest.TestCase):
    def test_404(self):
        self.assertRaisesRegex(
            luogu.NotFoundHttpException, r"^题目未找到$", luogu.Problem, "P0001"
        )

    def test_P1001(self):
        p = luogu.Problem("P1001")
        self.assertEqual(p.pid, "P1001")

    def test_equal(self):
        self.assertEqual(luogu.Problem("P1001"), luogu.Problem("P1001"))


if __name__ == "__main__":
    unittest.main()
