import abc
import string


class BaseFunctionError(Exception, abc.ABC):
    status_code: int
    description: str = None

    def __init__(self, message='', *, status_code=None, **params):
        self.params = params
        super(BaseFunctionError, self).__init__(message)
        self.status_code = status_code

        if self.description and super(BaseFunctionError, self).__str__():
            raise TypeError("Is not possible to set both message and description")

    def __str__(self):
        try:
            if self.description:
                if string.Formatter().parse(self.description):
                    return self.description % self.params
                else:
                    return self.description
            elif string.Formatter().parse(super(BaseFunctionError, self).__str__()):
                return self.description % self.params
            else:
                return super(BaseFunctionError, self).__str__()

        except (IndexError, TypeError) as e:
            msg = self.description or super(BaseFunctionError, self).__str__()
            if self.params:
                return f"{msg} {' '.join(str(i) for i in self.params)}"
            else:
                return msg


class SerializationError(BaseFunctionError):
    status_code = 500
    description = "Dont know how to serialize"


class BadRequestError(BaseFunctionError):
    status_code = 400
    description = "Bad Request"


class InternalServerError(BaseFunctionError):
    status_code = 500
    description = "Internal Server Error"


class ConflictError(BaseFunctionError):
    status_code = 409


class ResourceNotFoundError(BaseFunctionError):
    status_code = 404
