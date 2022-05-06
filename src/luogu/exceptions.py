class HttpException(Exception):
    pass


class AccessDeniedHttpException(HttpException):
    "403"


class NotFoundHttpException(HttpException):
    "404"
