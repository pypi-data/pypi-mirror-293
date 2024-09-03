from django.apps import apps
from django.contrib.auth import get_user_model
from rest_framework import serializers, validators


class UserEmailExistsSerializerValidator:
    def __call__(self, value):
        queryset = get_user_model().objects.filter(email=value)

        if not validators.qs_exists(queryset):
            raise serializers.ValidationError(
                "This field must be an email of a valid user."
            )


class EqualFieldsValidator:
    """
    This validator checks if all the fields passed in are equal

    Should be applied to the serializer class and not an individual
    field
    """

    def __init__(self, fields):
        self.fields = fields

    def __call__(self, attrs):
        hashset = set()
        for field in self.fields:
            hashset.add(attrs[field])

        if len(hashset) != 1:
            raise serializers.ValidationError(
                f"The fields - {','.join(self.fields)} must all have the same value"
            )
