"""
PyLuogu
=======

A model-based Python implement for Luogu API client

洛谷 API 客户端基于模型的 Python 实现
"""

import requests

USER_AGENT = "Mozilla/5.0"


class NotFoundHttpException(Exception):
    pass


def _get(url, params=None):
    r = requests.get(
        url,
        params=params,
        headers={"User-Agent": USER_AGENT, "X-Luogu-Type": "content-only"},
    )
    r.raise_for_status()
    data = r.json()
    if data["code"] == 404:
        raise NotFoundHttpException(data["currentData"]["errorMessage"])
    return data


class Model:
    def __str__(self) -> str:
        return repr(self.__dict__)


class User(Model):
    """用户

    :param uid: 用户 ID
    :type uid: int

    :var register_time: 注册时间
    :vartype register_time: int
    :var introduction: 个人介绍
    :vartype introduction: str
    :var prize: 获奖信息
    :vartype prize: list[Prize]
    :var blog_address: 个人博客地址
    :vartype blog_address: str
    :var passed_problem_count: 已通过题目数量
    :vartype passed_problem_count: int | None
    :var submitted_problem_count: 提交题目数量
    :vartype submitted_problem_count: int | None
    :var uid: 用户 ID
    :vartype uid: int
    :var name: 用户名
    :vartype name: str
    :var slogan: 个性签名
    :vartype slogan: str
    :var badge: 徽章
    :vartype badge: str | None
    :var is_admin: 是否管理员
    :vartype is_admin: bool
    :var is_banned: 是否被封禁
    :vartype is_banned: bool
    :var color: 颜色
    :vartype color: str
    :var ccf_level: CCF 等级
    :vartype ccf_level: int
    :var following_count: 关注数量
    :vartype following_count: int
    :var follower_count: 粉丝数量
    :vartype follower_count: int
    :var ranking: 排名
    :vartype ranking: int
    :var background: 封面
    :vartype background: str
    :var is_root: 是否为 root
    :vartype is_root: bool | None
    """

    class Prize(Model):
        """获奖信息

        :var year: 年份
        :vartype year: int
        :var contest_name: 竞赛名称
        :vartype contest_name: str
        :var prize: 奖项
        :vartype prize: str
        """

        def __init__(self, year: int, contestName: str, prize: str) -> None:
            self.year = year
            self.contest_name = contestName
            self.prize = prize

    def __init__(self, uid: int) -> None:
        self._raw_response_json: dict = _get(
            f"https://www.luogu.com.cn/user/{uid}"
        )
        user = self._raw_response_json["currentData"]["user"]
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
