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
    def __init__(self, uid) -> None:
        class Prize(Model):
            def __init__(self, year, contestName, prize) -> None:
                self.year: int = year
                self.contest_name: str = contestName
                self.prize: str = prize

        self._raw_response_json: dict = _get(
            f"https://www.luogu.com.cn/user/{uid}"
        )
        user = self._raw_response_json["currentData"]["user"]
        self.register_time: int = user["registerTime"]
        self.introduction: str = user["introduction"]
        self.prize = [Prize(**prize) for prize in user["prize"]]
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
