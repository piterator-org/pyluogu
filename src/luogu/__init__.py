"""
PyLuogu
=======

A model-based Python implement for Luogu API client

洛谷 API 客户端基于模型的 Python 实现
"""

from html.parser import HTMLParser
from http.cookies import SimpleCookie
from io import BytesIO
from pprint import pformat

import requests
import requests.cookies

USER_AGENT = "Mozilla/5.0"


def cached_method(func):
    def wrapper(self, *args):
        if not hasattr(self, "__cache"):
            self.__cache = {}
        cache = self.__cache
        if args not in cache:
            cache[args] = func(self, *args)
        return cache[args]

    return wrapper


class HttpException(Exception):
    pass


class AccessDeniedHttpException(HttpException):
    "403"


class NotFoundHttpException(HttpException):
    "404"


def _dict_without_underscores(d: dict):
    return dict(filter(lambda i: not i[0].startswith("_"), d.items()))


class Model:
    _session = requests.Session()

    def _get(self, url, params=None):
        r = self._session.get(
            url,
            params=params,
            headers={"User-Agent": USER_AGENT, "X-Luogu-Type": "content-only"},
        )
        r.raise_for_status()
        data = r.json()
        if data["code"] == 404:
            raise NotFoundHttpException(data["currentData"]["errorMessage"])
        elif data["code"] == 403:
            raise AccessDeniedHttpException(
                data["currentData"]["errorMessage"]
            )
        elif data["code"] >= 400:
            raise HttpException(data["currentData"]["errorMessage"])
        return data

    def __repr__(self):
        return pformat(
            _dict_without_underscores(self.__dict__),
            # sort_dicts=False,  # Python 3.8+ only
        )

    def __eq__(self, other):
        if hasattr(self, "_current_data") and hasattr(other, "_current_data"):
            return self._current_data == other._current_data
        if type(other) is type(self):
            return _dict_without_underscores(
                self.__dict__
            ) == _dict_without_underscores(other.__dict__)
        else:
            super().__eq__(other)


class LazyList(list):
    def __init__(self, iterable, getitem=lambda i: i):
        if iterable is None:
            super().__init__()
        else:
            super().__init__(iterable)
        self._getitem = getitem

    @cached_method
    def __getitem__(self, index):
        return self._getitem(super().__getitem__(index))


class User(Model):
    """用户

    :param uid: 用户 ID
    :type uid: int | str

    :raises NotFoundHttpException: 用户未找到

    :var int register_time: 注册时间
    :var str introduction: 个人介绍
    :var list[Prize] prize: 获奖信息
    :var str blog_address: 个人博客地址
    :var passed_problem_count: 已通过题目数量
    :vartype passed_problem_count: int | None
    :var submitted_problem_count: 提交题目数量
    :vartype submitted_problem_count: int | None
    :var int uid: 用户 ID
    :var str name: 用户名
    :var str slogan: 个性签名
    :var badge: 徽章
    :vartype badge: str | None
    :var bool is_admin: 是否管理员
    :var bool is_banned: 是否被封禁
    :var str color: 颜色
    :var int ccf_level: CCF 等级
    :var int following_count: 关注数量
    :var int follower_count: 粉丝数量
    :var int ranking: 排名
    :var str background: 封面
    :var is_root: 是否为 root
    :vartype is_root: bool | None
    :var passed_problems: 已通过的题目
    :vartype passed_problems: list[Problem] | None
    :var submitted_problems: 尝试过的题目
    :vartype submitted_problems: list[Problem] | None
    """

    class Prize(Model):
        """获奖信息

        :var int year: 年份
        :var str contest_name: 竞赛名称
        :var str prize: 奖项
        """

        def __init__(self, year: int, contestName: str, prize: str) -> None:
            self.year = year
            self.contest_name = contestName
            self.prize = prize

    def __init__(self, uid: "int | str") -> None:
        self._current_data: dict[str] = self._get(
            f"https://www.luogu.com.cn/user/{uid}"
        )["currentData"]

        user: dict[str] = self._current_data["user"]
        self.register_time: int = user["registerTime"]
        self.introduction: str = user["introduction"]
        self.prize = [self.Prize(**prize) for prize in user["prize"]]
        self.blog_address: str = user["blogAddress"]
        self.passed_problem_count: int | None = user["passedProblemCount"]
        self.submitted_problem_count: int | None = user[
            "submittedProblemCount"
        ]
        self.uid: int = user["uid"]
        self.name: str = user["name"]
        self.slogan: str = user["slogan"]
        self.badge: str | None = user["badge"]
        self.is_admin: bool = user["isAdmin"]
        self.is_banned: bool = user["isBanned"]
        self.color: str = user["color"]
        self.ccf_level: int = user["ccfLevel"]
        self.following_count: int = user["followingCount"]
        self.follower_count: int = user["followerCount"]
        self.ranking: int = user["ranking"]
        self.background: str = user["background"]
        self.is_root: bool = user["isRoot"] if "isRoot" in user else None

        def get_problem(p: dict) -> Problem:
            return Problem(p["pid"])

        self._passed_problems: list[dict] = (
            self._current_data["passedProblems"]
            if "passedProblems" in self._current_data
            else None
        )
        self.passed_problems: list[Problem] = LazyList(
            self._passed_problems,
            get_problem,
        )
        self._submitted_problems: list[dict] = (
            self._current_data["submittedProblems"]
            if "submittedProblems" in self._current_data
            else None
        )
        self.submitted_problems: list[Problem] = LazyList(
            self._submitted_problems,
            get_problem,
        )


class Problem(Model):
    """题目

    :param str pid: 题目 ID

    :raises AccessDeniedHttpException: 您无权查看该题目
    :raises NotFoundHttpException: 题目未找到

    :var str background: 题目背景
    :var str description: 题目描述
    :var str input_format: 输入格式
    :var str output_format: 输出格式
    :var samples: 样例
    :vartype samples: list[tuple[str, str]]
    :var str hint: 说明/提示
    :var User provider: 题目提供者
    :var list[Attachment] attachments: 附件
    :var bool can_edit: 可编辑
    :var limits: 限制
    :vartype limits: dict[str, list[int]]
    :var str std_code: 标准代码
    :var list[int] tags: 标签
    :var bool wants_translation: 需要翻译
    :var int total_submit: 总提交
    :var int total_accepted: 总通过
    :var int flag:
    :var str pid: 题目 ID
    :var str title: 题目标题
    :var int difficulty: 难度
    :var int full_score: 满分
    :var str type: 题目类型
    """

    def __init__(self, pid: str) -> None:
        self._current_data: dict[str] = self._get(
            f"https://www.luogu.com.cn/problem/{pid}"
        )["currentData"]

        problem: dict[str] = self._current_data["problem"]
        self.background: str = problem["background"]
        self.description: str = problem["description"]
        self.input_format: str = problem["inputFormat"]
        self.output_format: str = problem["outputFormat"]
        self.samples: list[tuple[str, str]] = [
            (s[0], s[1]) for s in problem["samples"]
        ]
        self.hint: str = problem["hint"]
        self._provider: str = problem["provider"]
        self.attachments = [
            self.Attachment(**attachment)
            for attachment in problem["attachments"]
        ]
        self.can_edit: bool = problem["canEdit"]
        self.limits: dict[str, list[int]] = problem["limits"]
        self.std_code: str = problem["stdCode"]
        self.tags: list[int] = problem["tags"]
        self.wants_translation: bool = problem["wantsTranslation"]
        self.total_submit: int = problem["totalSubmit"]
        self.total_accepted: int = problem["totalAccepted"]
        self.flag: int = problem["flag"]
        self.pid: str = problem["pid"]
        self.title: str = problem["title"]
        self.difficulty: int = problem["difficulty"]
        self.full_score: int = problem["fullScore"]
        self.type: str = problem["type"]

    class Attachment(Model):
        """附件

        :var str download_link: 下载链接
        :var int size: 大小
        :var int upload_time: 上传时间
        :var str id: ID
        :var str filename: 文件名
        """

        def __init__(
            self,
            downloadLink: str,
            size: int,
            uploadTime: int,
            id: str,
            filename: str,
        ) -> None:
            self.download_link = downloadLink
            self.size = size
            self.upload_time = uploadTime
            self.id = id
            self.filename = filename

    @property
    @cached_method
    def provider(self):
        return User(self._provider["uid"])


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
        self.Problem._session = self.session
        self.User._session = self.session

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

        class HTMLCSRFTokenParser(HTMLParser):
            def handle_starttag(self, tag, attrs):
                attrs = dict(attrs)
                try:
                    if tag == "meta" and attrs["name"] == "csrf-token":
                        raise StopIteration(attrs["content"])
                except KeyError:
                    pass

        r = self.session.get("https://www.luogu.com.cn/auth/login")
        r.raise_for_status()
        try:
            HTMLCSRFTokenParser().feed(r.text)
        except StopIteration as csrf_token:
            r = self.session.post(
                "https://www.luogu.com.cn/api/auth/userPassLogin",
                headers={
                    "x-csrf-token": str(csrf_token),
                },
                json={
                    "username": username,
                    "password": password,
                    "captcha": captcha,
                },
            )
            r.raise_for_status()
            return r.json()

    class Problem(Problem):
        pass

    class User(User):
        pass
