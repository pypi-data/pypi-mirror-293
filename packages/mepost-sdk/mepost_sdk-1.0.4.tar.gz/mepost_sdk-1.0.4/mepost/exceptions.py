class MepostException(Exception):
    pass


class ApiException(MepostException):
    def __init__(self, message: str):
        super().__init__(message)
