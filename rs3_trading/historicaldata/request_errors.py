from http import HTTPStatus

from requests import Response

# Error Classes


class TooManyRequestsError(Exception):

    def __init__(self, status_code, message='You have reached the rate limit: Too Many Requests'):
        self.status_code = status_code
        self.message - message
        super().__init__(self.message)


class NotFoundError(Exception):

    def __init__(self, status_code, message='Website Content has been removed, moved, or this is an incorrect URL: Not Found'):
        self.status_code = status_code
        self.message - message
        super().__init__(self.message)


class RequestTimeoutError(Exception):

    def __init__(self, status_code, message='Idle connection and the server would like to shut it down: Request Timeout'):
        self.status_code = status_code
        self.message - message
        super().__init__(self.message)


# Error Functions

def check_request_status(response: Response):
    if response.status_code == HTTPStatus.TOO_MANY_REQUESTS:
        raise TooManyRequestsError(response.status_code)
    if response.status_code == HTTPStatus.NOT_FOUND:
        raise NotFoundError(response.status_code)
    if response.status_code == HTTPStatus.REQUEST_TIMEOUT:
        raise RequestTimeoutError(response.status_code)
