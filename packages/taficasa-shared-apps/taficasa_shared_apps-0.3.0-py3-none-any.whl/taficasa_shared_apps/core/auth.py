from django.conf import settings
from django.utils.translation import gettext_lazy as _
from knox.auth import TokenAuthentication
from rest_framework import exceptions, request


class CookieBasedTokenAuthentication(TokenAuthentication):
    def _get_auth_cookie_token(self, request):
        if settings.AUTH_COOKIE_NAME in request.COOKIES:
            # Note str needs to be encoded to work with knox auth method
            auth_token = request.COOKIES[settings.AUTH_COOKIE_NAME].encode("utf-8")
            return auth_token
        msg = _("Authentication Cookie Not Provided")
        raise exceptions.AuthenticationFailed(msg)

    def authenticate(self, request: request.Request):
        # Use regular token based auth for local env excluding testing and for
        # calls made to internal urls
        if (settings.LOCAL and not settings.TESTING) or request.path.startswith(
            "/v1/internal"
        ):
            response = super().authenticate(request)
            # Special check to make sure that on non local env only
            # bot users can successfully log in without cookies
            if response and not settings.LOCAL and not response[0].is_bot:
                raise exceptions.AuthenticationFailed(_("Only Bot users can login"))
            return response
        else:
            auth_cookie_token = self._get_auth_cookie_token(request=request)
            user, auth_token = self.authenticate_credentials(auth_cookie_token)
            if user.is_bot:
                raise exceptions.AuthenticationFailed(
                    _("Bot users can't login with cookies")
                )
            return user, auth_token
