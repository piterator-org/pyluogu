from datetime import datetime

from ..utils import LazyList, cached_method
from . import Model


class User(Model):
    """用户

    :param uid: 用户 ID
    :type uid: int | str

    :raises NotFoundHttpException: 用户未找到

    :var datetime.datetime register_time: 注册时间
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
        self.register_time = datetime.fromtimestamp(user["registerTime"])
        self.introduction: str = user["introduction"]
        self.prize = [self.Prize(**prize) for prize in user["prize"]]
        self.blog_address: str = user["blogAddress"]
        self.passed_problem_count: int | None = user["passedProblemCount"]
        self.submitted_problem_count: int | None = user["submittedProblemCount"]
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

        self._passed_problems: list[dict] = (
            self._current_data["passedProblems"]
            if "passedProblems" in self._current_data
            else None
        )
        self.passed_problems: list[Problem] = (
            LazyList(
                Problem,
                [p["pid"] for p in self._passed_problems],
            )
            if self._passed_problems
            else []
        )
        self._submitted_problems: list[dict] = (
            self._current_data["submittedProblems"]
            if "submittedProblems" in self._current_data
            else None
        )
        self.submitted_problems: list[Problem] = (
            LazyList(
                Problem,
                [p["pid"] for p in self._submitted_problems],
            )
            if self._submitted_problems
            else []
        )

    @property
    def id(self):
        return self.uid

    @classmethod
    def search(cls, keyword: str) -> "list[User]":
        """根据 UID 或用户名搜索用户

        :param str keyword: 搜索关键字
        """
        users = cls._get(
            "https://www.luogu.com.cn/api/user/search",
            {"keyword": keyword},
            False,
        )["users"]
        return LazyList(User, [u["uid"] for u in users if u is not None])


class ProblemList(Model):
    """题目列表

    :param str type: 题库
    :param int page: 页码
    :param str keyword: 关键词
    :param int difficulty: 难度
    :param str tag: 标签
    :param bool content: 搜索题目内容

    :var str type: 题库
    :var int page: 页码
    :var list problems: 题目列表
    :var int problem_count: 题目数量
    """

    def __init__(self, page: int = 1, type: str = 'P', keyword: str = '', difficulty: int | str = '', tag: str = '', content: bool = False) -> None:
        self._current_data: dict[str] = self._get(
            f"https://www.luogu.com.cn/problem/list?page={page}&type={type}&keyword={keyword}&difficulty={difficulty}&tag={tag}&content={'true' if content else 'false'}&_contentOnly=1"
        )["currentData"]

        self.page: int = self._current_data['page']
        self.type = type

        problems: dict = self._current_data['problems']
        self.problem_count = problems['count']
        self.problems = problems['result']


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
        self.samples: list[tuple[str, str]] = [(s[0], s[1]) for s in problem["samples"]]
        self.hint: str = problem["hint"]
        self._provider: str = problem["provider"]
        self.attachments = [
            self.Attachment(**attachment) for attachment in problem["attachments"]
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
        :var datetime.datetime upload_time: 上传时间
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
            self.upload_time = datetime.fromtimestamp(uploadTime)
            self.id = id
            self.filename = filename

    @property
    def id(self):
        return self.pid

    @property
    @cached_method
    def provider(self):
        return User(self._provider["uid"])
