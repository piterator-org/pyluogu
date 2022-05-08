from datetime import datetime

from ..utils import cached_method
from . import Model
from .main import User


class Paste(Model):
    """剪贴板

    :param str id: 剪贴板 ID

    :var str data: 内容
    :var str id: 剪贴板 ID
    :var User user: 用户
    :var datetime.datetime time: 时间
    :var bool public: 是否公开
    """

    def __init__(self, id: str) -> None:
        self._current_data: dict[str] = self._get(
            f"https://www.luogu.com.cn/paste/{id}"
        )["currentData"]

        paste: dict[str] = self._current_data["paste"]
        self.data: str = paste["data"]
        self.id: str = paste["id"]
        self._user: dict[str] = paste["user"]
        self.time = datetime.fromtimestamp(paste["time"])
        self.public: bool = paste["public"]

    @property
    @cached_method
    def user(self) -> User:
        return User(self._user["uid"])

    def delete(self) -> str:
        """删除剪贴板

        :returns: 剪贴板 ID
        :rtype: str
        """
        return self._post(f"https://www.luogu.com.cn/paste/delete/{self.id}")["id"]

    def edit(self, data: str = None, public: bool = None):
        """编辑剪贴板

        :param str data: 剪贴板内容
        :param bool public: 是否公开

        :returns: 剪贴板 ID
        :rtype: str
        """
        r = self._post(
            f"https://www.luogu.com.cn/paste/edit/{self.id}",
            {"data": data, "public": public},
        )
        if data is not None:
            self.data = data
        if public is not None:
            self.public = public
        return r["id"]

    @classmethod
    def new(cls, data: str, public: bool = None) -> "Paste":
        """新建剪贴板

        :param str data: 剪贴板内容
        :param bool public: 值为真时表示公开剪贴板，否则表示私有剪贴板

        :rtype: Session.Paste
        """
        r = cls._post(
            "https://www.luogu.com.cn/paste/new",
            {"data": data, "public": public},
        )
        return cls(r["id"])
