from typing import cast

ExcMeta: type = type(Exception)


class BaseException(Exception):
    message: str | None = None

    def __init__(self, *args: object, **kwargs: object) -> None:
        try:
            (message, *extra_args) = args
            if isinstance(message, str):
                self.message = message
        except ValueError:
            pass

        for key, val in kwargs.items():
            setattr(self, key, val)


class ProgrammingError(BaseException):
    pass


class ServiceExceptionMeta(ExcMeta):
    registry: dict[str, type] = {}

    def __new__(cls, name, bases, namespace, **kwargs):
        if name in cls.registry:
            raise ProgrammingError("Duplicate exception name in registry.")
        cls.registry[name] = super().__new__(cls, name, bases, namespace, **kwargs)
        return cls.registry[name]

    @classmethod
    def get_exception_class(cls, name):
        return cls.registry[name]


class ServiceException(BaseException, metaclass=ServiceExceptionMeta):
    http_status_code: int = 500
    http_error_name: str = "server_error"

    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        kwargs.setdefault("http_status_code", self.http_status_code)
        kwargs.setdefault("http_error_name", self.http_error_name)
        super().__init__(
            *args,
            **kwargs,
        )
        self.args = args
        self.kwargs = kwargs

    @classmethod
    def from_dict(cls, dict_: dict) -> "ServiceException":
        name = cast(str, dict_.get("name"))
        exc_class = ServiceExceptionMeta.get_exception_class(name)
        args = cast(tuple, dict_.get("args"))
        kwargs = cast(dict, dict_.get("kwargs"))
        return exc_class(*args, **kwargs)

    def to_dict(self):
        return {
            "args": self.args,
            "kwargs": self.kwargs,
            "name": self.__class__.__name__,
        }


class InvalidToken(ServiceException):
    message = "The supplied token is invalid."
    http_status_code = 401
    http_error_name = "invalid_token"


class InvalidCredentials(ServiceException):
    message = "Authentication credentials rejected."
    http_status_code = 401
    http_error_name = "invalid_credentials"


class Forbidden(ServiceException):
    message = "Authentication credentials indicate insufficient permissions."
    http_status_code = 403
    http_error_name = "forbidden"
