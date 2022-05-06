from http.cookies import SimpleCookie
from io import BytesIO

import requests

from .constants import USER_AGENT
from .models import Paste, Problem, User
from .utils import get_csrf_token


class Session:
    """会话

    :param cookies: Cookies
    :type cookies: str | dict[str, str] | None

    :var requests.cookies.RequestsCookieJar cookies: Cookies
    :var requests.Session session: 会话
    """

    def __init__(self, cookies: "str | dict[str, str] | None" = None) -> None:
        self.cookies = requests.cookies.cookiejar_from_dict(
            {k: v.value for k, v in SimpleCookie(cookies).items()}
        )
        self.session = requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self.session.headers["referer"] = "http://www.luogu.com.cn/"
        self.session.cookies = self.cookies
        self.Paste._session = self.session
        self.Problem._session = self.session
        self.User._session = self.session

    class Paste(Paste):
        pass

    class Problem(Problem):
        pass

    class User(User):
        pass

    def captcha(self, show: bool = True) -> bytes:
        """获取验证码

        :param bool show:
            值为真时使用 :meth:`PIL.Image.Image.show` 显示验证码；否则仅返回图片的二进制数据

        :rtype: bytes
        """
        r = self.session.get("https://www.luogu.com.cn/api/verify/captcha")
        r.raise_for_status()
        if show:
            from PIL import Image

            Image.open(BytesIO(r.content)).show()
        return r.content

    def login(self, username: str, password: str, captcha: str) -> "dict[str]":
        """登录

        :param str username: 用户名
        :param str password: 密码
        :param str captcha: 验证码

        :rtype: dict[str]
        """

        r = self.session.post(
            "https://www.luogu.com.cn/api/auth/userPassLogin",
            headers={
                "x-csrf-token": get_csrf_token(
                    self.session, "https://www.luogu.com.cn/auth/login"
                ),
            },
            json={
                "username": username,
                "password": password,
                "captcha": captcha,
            },
        )
        r.raise_for_status()
        return r.json()

    def logout(self) -> "dict[str, bool]":
        """登出

        :rtype: dict[str, bool]
        """
        r = self.session.post(
            "https://www.luogu.com.cn/api/auth/logout",
            headers={"x-csrf-token": get_csrf_token(self.session)},
        )
        r.raise_for_status()
        return r.json()
