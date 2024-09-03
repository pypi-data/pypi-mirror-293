from typing import Optional

from rest_framework import exceptions, status


class BaseAPIErrorCode:
    code: str
    detail: str


class APIServiceError(exceptions.APIException):
    def __init__(
        self,
        error_code: BaseAPIErrorCode,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        """
        General error class for service classes, uses status code 400

        params - message: message to show the api user
                 describing the error

                 code: unique str error code for this error
        """
        super().__init__(
            detail=error_code.detail,
            code=error_code,
        )
        self.status_code = status_code
        self.error_code = error_code


class APIValidationError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST

    def __init__(
        self,
        message: str,
    ):
        """
        General error class for validation errors, uses status code 400

        params - message: message to show the api user
                 describing the error
        """
        super().__init__(
            detail=message,
            code="api_validation_error",
        )


class GenericInternalError(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str, code: str = "generic_internal_error"):
        """
        Generic error class for internal server errors, uses status code 500

        params - message: message to show the api user
                 describing the error

                 code: unique str error code for this error
        """

        super().__init__(
            detail=message,
            code=code,
        )


class InvalidRequestError(exceptions.APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = "Invalid Request."
    default_code = "invalid_request"

    def __init__(self, message: Optional[str] = None, code: Optional[int] = None):
        """
        General error class for cases when a request
        contains invalid data or cannot be processed.
        """

        super().__init__(
            detail=message or self.default_detail,
            code=code or self.default_code,
        )
