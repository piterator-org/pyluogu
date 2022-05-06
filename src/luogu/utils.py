from html.parser import HTMLParser

import requests


def dict_without_underscores(d: dict):
    return dict(filter(lambda i: not i[0].startswith("_"), d.items()))


def get_csrf_token(
    session: requests.Session, url: str = "https://www.luogu.com.cn/"
) -> str:
    class HTMLCSRFTokenParser(HTMLParser):
        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            try:
                if tag == "meta" and attrs["name"] == "csrf-token":
                    raise StopIteration(attrs["content"])
            except KeyError:
                pass

    r = session.get(url)
    r.raise_for_status()
    try:
        HTMLCSRFTokenParser().feed(r.text)
    except StopIteration as csrf_token:
        return str(csrf_token)


def cached_method(func):
    def wrapper(self, *args):
        if not hasattr(self, "__cache"):
            self.__cache = {}
        cache = self.__cache
        if args not in cache:
            cache[args] = func(self, *args)
        return cache[args]

    return wrapper


class LazyList(list):
    def __init__(self, model, args):
        super().__init__(args)
        self._model = model

    @cached_method
    def __getitem__(self, index):
        return self._model(super().__getitem__(index))

    def __iter__(self):
        for i in super().__iter__():
            yield self._model(i)

    def __repr__(self) -> str:
        return (
            "["
            + ",\n ".join([f"{self._model.__name__}({i})" for i in list.__iter__(self)])
            + "]"
        )
