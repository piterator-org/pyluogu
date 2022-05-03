import os
import unittest

import requests

import luogu
from requests.cookies import RequestsCookieJar


class TestUser(unittest.TestCase):
    def test_404(self):
        self.assertRaisesRegex(
            luogu.NotFoundHttpException, r"^用户未找到$", luogu.User, 0
        )

    def test_equal(self):
        u = luogu.User(1)
        self.assertEqual(u, luogu.User.search("kkksc03")[0])
        self.assertNotEqual(u, luogu.User(2))
        self.assertNotEqual(u, 1)

    def test_repr(self):
        u = luogu.User(3)
        self.assertEqual({**eval(repr(u)), **u.__dict__}, u.__dict__)

    def test_kkksc03(self):
        u = luogu.User(1)
        self.assertIn(luogu.User.Prize(2019, "CSP入门", "一等奖"), u.prize)
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
    def test_403(self):
        self.assertRaisesRegex(
            luogu.AccessDeniedHttpException,
            r"^您无权查看该题目$",
            luogu.Problem,
            "T1000",
        )

    def test_404(self):
        self.assertRaisesRegex(
            luogu.NotFoundHttpException, r"^题目未找到$", luogu.Problem, "P0001"
        )

    def test_equal(self):
        p = luogu.Problem("P1000")
        self.assertEqual(p, luogu.Problem("P1000"))
        self.assertNotEqual(p, luogu.Problem("P1001"))

    def test_P1001(self):
        p = luogu.Problem("P1001")
        self.assertEqual(p.pid, "P1001")

    def test_attachment(self):
        attachment = luogu.Problem("P7912").attachments[0]
        self.assertIsInstance(attachment, luogu.Problem.Attachment)
        self.assertEqual(attachment.filename, "fruit.zip")


class TestSession(unittest.TestCase):
    def test_creation(self):
        s = luogu.Session("__client_id=0123456789abcdef; _uid=0")
        self.assertIsInstance(s.cookies, RequestsCookieJar)
        self.assertIs(s.session.cookies, s.cookies)
        self.assertIs(s.Problem._session, s.session)
        self.assertIs(s.User._session, s.session)

    def login(self, s: luogu.Session):
        r = requests.post(
            "https://luogu-captcha-bypass.piterator.com/predict",
            data=s.captcha(show=False),
            headers={"Content-Type": "image/jpeg"},
        )
        r.raise_for_status()
        self.assertEqual(
            s.login(
                os.environ["LUOGU_USERNAME"],
                os.environ["LUOGU_PASSWORD"],
                r.text,
            )["username"],
            os.environ["LUOGU_USERNAME"],
        )

    def test_login(self):
        s = luogu.Session()
        # s.captcha()
        try:
            self.login(s)
        except requests.HTTPError:
            self.login(s)

        p = s.Paste.new("Hello, world!")
        self.assertEqual(p.user.name, os.environ["LUOGU_USERNAME"])
        self.assertEqual(p.delete(), p.id)

        self.assertTrue(s.logout()["_empty"])


if __name__ == "__main__":
    unittest.main()
