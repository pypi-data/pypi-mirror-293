from functools import wraps

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied


def ensure_same_user(view_func):
    """
    A decorator that ensures that the user passed
    in the request using the key 'user' matches
    the user that is actually authenticated and that is
    initiating the request.

    Raises Permission Denied Error
    """

    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # try to get the user passed in the request data
        queryset = get_user_model().filter(email=request.data["user"])

        if not bool(queryset):
            raise PermissionDenied

        user_instance = queryset.get()

        if str(user_instance.id) != str(request.user.id):
            raise PermissionDenied

        return view_func(request, *args, **kwargs)
