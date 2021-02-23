import abc
import string


class BaseFunctionError(Exception, abc.ABC):
    status_code: int
    message: str = None

    def __init__(self, message: str = None, *, status_code: int = None, **params):
        super(BaseFunctionError, self).__init__(message)
        self.params = params
        self.status_code = status_code
        if message:
            self.message = message

    def __str__(self):
        parsed = {tup[1] for tup in string.Formatter().parse(self.message) if tup[1] is not None}
        has_params = len(parsed) > 0
        _parsed = parsed.copy()
        for param in parsed:
            if param in self.params:
                _parsed.remove(param)
        len_parsed = len(_parsed)
        if len_parsed != 0:
            raise TypeError(
                f"{self.__class__.__name__} missing {len_parsed} required keyword-only argument: {_parsed}")
        if has_params:
            return self.message.format(**self.params)
        else:
            return self.message


class SerializationError(BaseFunctionError):
    status_code = 500
    message = "Dont know how to serialize"


class BadRequestError(BaseFunctionError):
    status_code = 400
    message = "Bad Request"


class InternalServerError(BaseFunctionError):
    status_code = 500
    message = "Internal Server Error"


class ConflictError(BaseFunctionError):
    status_code = 409


class ResourceNotFoundError(BaseFunctionError):
    status_code = 404
