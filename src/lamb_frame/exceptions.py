class BaseLambdaError(Exception):
    status_code: int
    description: str

    def __str__(self):
        if len(self.args):
            try:
                return self.description % self.args
            except (IndexError, TypeError) as e:
                return f"{self.description} {' '.join(self.args)}"
        if hasattr(self, 'description') and self.description:
            return self.description
        else:
            return str(self)


class SerializationError(BaseLambdaError):
    status_code = 500
    description = "Dont know how to serialize"


class BadRequestError(BaseLambdaError):
    status_code = 400
    description = "Bad Request"


class InternalServerError(BaseLambdaError):
    status_code = 500
    description = "Internal Server Error"
