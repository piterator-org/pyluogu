import requests

from ..constants import USER_AGENT
from ..exceptions import AccessDeniedHttpException, HttpException, NotFoundHttpException
from ..utils import dict_without_underscores, get_csrf_token


class Model:
    _session = requests.Session()
    _session.headers["User-Agent"] = USER_AGENT

    @classmethod
    def _get(cls, url: str, params: dict = None, check: bool = True) -> "dict[str]":
        r = cls._session.get(
            url,
            params=params,
            headers={"X-Luogu-Type": "content-only"},
        )
        r.raise_for_status()
        data = r.json()
        if check:
            if data["code"] == 404:
                raise NotFoundHttpException(data["currentData"]["errorMessage"])
            elif data["code"] == 403:
                raise AccessDeniedHttpException(data["currentData"]["errorMessage"])
            elif data["code"] >= 400:
                raise HttpException(data["currentData"]["errorMessage"])
        return data

    @classmethod
    def _post(cls, url: str, data: dict = None) -> "dict[str]":
        r = cls._session.post(
            url,
            json=data,
            headers={
                "x-csrf-token": get_csrf_token(cls._session),
            },
        )
        r.raise_for_status()
        return r.json()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.id})"

    def __eq__(self, other):
        if hasattr(self, "_current_data") and hasattr(other, "_current_data"):
            return self._current_data == other._current_data
        if type(other) is type(self):
            return dict_without_underscores(self.__dict__) == dict_without_underscores(
                other.__dict__
            )
        else:
            super().__eq__(other)
