import datetime

import google.auth
import google.auth.compute_engine
import google.auth.transport.requests
from django.conf import settings
from django.core.cache import cache
from django.utils.deconstruct import deconstructible
from storages.backends.gcloud import GoogleCloudStorage


@deconstructible
class BaseStorage(GoogleCloudStorage):
    CACHE_KEY = "GoogleCloudStorageAccessToken.signing_extra_params"

    def __init__(self, dev_override=True, *args, **kwargs):
        # Override the bucket for non production environments
        if dev_override and not settings.PROD:
            kwargs["bucket_name"] = "dev-bucket.taficasa.com"
        super().__init__(*args, **kwargs)

    def url(self, name, parameters=None):
        """
        This function loads in extra credential params to
        the call for signing urls

        It is a workaround for not being able to
        use service accounts to sign urls.

        Workaround inferred from github issue below
        -> https://github.com/jschneier/django-storages/issues/941#issuecomment-797724786
        """

        # We only need this workaround when running in cloud run where we have a
        # service account attached.
        if not settings.LOCAL or settings.TESTING:
            extra_params = self.get_extra_signing_credentials()
            return super().url(name, parameters=extra_params)
        else:
            return super().url(name)

    def get_extra_signing_credentials(self):
        value = cache.get(self.CACHE_KEY)
        if value is not None:
            expiry, extra_params = value
            if expiry > datetime.datetime.utcnow():
                return extra_params

        credentials, project_id = google.auth.default()
        auth_req = google.auth.transport.requests.Request()
        credentials.refresh(auth_req)
        extra_params = {
            "service_account_email": credentials.service_account_email,
            "access_token": credentials.token,
            "credentials": credentials,
        }

        cache.set(self.CACHE_KEY, (credentials.expiry, extra_params))
        return extra_params


@deconstructible
class MediaStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        kwargs["bucket_name"] = "media.taficasa.com"
        super().__init__(*args, **kwargs)


@deconstructible
class StaticFilesStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        if settings.PROD:
            kwargs["bucket_name"] = "static.taficasa.com"
        else:
            kwargs["bucket_name"] = "dev.static.taficasa.com"
        super().__init__(dev_override=False, *args, **kwargs)


@deconstructible
class SupplyChainStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        kwargs["bucket_name"] = "supplychain.taficasa.com"
        super().__init__(*args, **kwargs)


@deconstructible
class OrganizationsStorage(BaseStorage):
    def __init__(self, *args, **kwargs):
        kwargs["bucket_name"] = "organizations.taficasa.com"
        super().__init__(*args, **kwargs)
