from rest_framework.views import exception_handler as default_exception_handler


def api_exception_handler(exception, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = default_exception_handler(exception, context)

    # Now add the HTTP status code to the response.
    if response is not None:
        response.data["status_code"] = response.status_code

    # TODO If exception should be logged then do so
    if getattr(exception, "should_log", None):
        # Do some logging
        pass

    # TODO If exception should raise alert
    if getattr(exception, "raise_alert", None):
        # Do some alerting
        pass

    return response
