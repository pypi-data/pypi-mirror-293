import uuid

from bson import ObjectId
from bson.errors import InvalidId
from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str
from rest_framework import serializers


class UserIdValidator:
    """
    This validator checks if the userid passed in is valid
    and if so returns a user object. This validator requires
    that context be passed into the serializer with the request
    instance.

    Should be applied to an individual field
    """

    requires_context = True

    def __init__(self, check_organization: bool = False):
        self.check_organization = check_organization

    def __call__(self, value, serializer_field):
        pass


class UserIdSerializerField(serializers.UUIDField):
    def __init__(self, check_organization: bool = False, **kwargs):
        self.check_organization = check_organization
        super().__init__(**kwargs)

    def to_representation(self, value):
        if hasattr(value, "userid"):
            return str(value.userid)
        else:
            return str(value)

    def to_internal_value(self, data):
        # Lazy loading all models needed
        Organization = apps.get_model(
            app_label="organization_management", model_name="Organization"
        )

        try:
            if isinstance(data, str):
                uuid_value = uuid.UUID(hex=data)
            else:
                raise serializers.ValidationError(
                    f"This userid '{data}' is not a uuid string"
                )

            user = get_user_model().objects.filter(userid=uuid_value).get()

            if self.check_organization:
                request = self.context.get("request")
                if not request:
                    raise serializers.ValidationError(
                        "Request must be passed into the serializer context"
                        " to use the UserIdSerializerField field"
                    )

                # Check the request url captured kwargs and request data
                organiaztion_id = request.data.get(
                    "organization_id"
                ) or request.resolver_match.kwargs.get("organization_id")

                if not organiaztion_id:
                    raise serializers.ValidationError("Organization ID not provided")

                try:
                    organization = Organization.objects.filter(
                        organization_id=organiaztion_id
                    ).get()
                    if not organization.is_member(user):
                        raise serializers.ValidationError(
                            f"This userid '{data}' does not belong to the"
                            " organization being accessed"
                        )

                except Organization.DoesNotExist:
                    raise serializers.ValidationError(
                        "Organization being accessed is invalid"
                    )
            return user
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError(f"This userid '{data}' is invalid")


class ObjectIdField(serializers.Field):
    """Field for ObjectId values"""

    def to_internal_value(self, value):
        try:
            return ObjectId(smart_str(value))
        except InvalidId:
            raise serializers.ValidationError("'%s' is not a valid ObjectId" % value)

    def to_representation(self, value):
        return smart_str(value)
