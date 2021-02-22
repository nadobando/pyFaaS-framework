import abc
import string


class BaseLambdaError(Exception, abc.ABC):
    status_code: int
    description: str = None

    def __init__(self, message='', *, status_code=None, **params):
        self.params = params
        super(BaseLambdaError, self).__init__(message)
        self.status_code = status_code

        if self.description and super(BaseLambdaError, self).__str__():
            raise TypeError("Is not possible to set both message and description")

    def __str__(self):
        try:
            if self.description:
                if string.Formatter().parse(self.description):
                    return self.description % self.params
                else:
                    return self.description
            elif string.Formatter().parse(super(BaseLambdaError, self).__str__()):
                return self.description % self.params
            else:
                return super(BaseLambdaError, self).__str__()

        except (IndexError, TypeError) as e:
            msg = self.description or super(BaseLambdaError, self).__str__()
            if self.params:
                return f"{msg} {' '.join(str(i) for i in self.params)}"
            else:
                return msg


class SerializationError(BaseLambdaError):
    status_code = 500
    description = "Dont know how to serialize"


class BadRequestError(BaseLambdaError):
    status_code = 400
    description = "Bad Request"


class InternalServerError(BaseLambdaError):
    status_code = 500
    description = "Internal Server Error"
