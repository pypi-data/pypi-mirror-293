from enum import StrEnum

from core.mixins import ModelChoiceMixin
from django.db import models


class CustomCurrencyField(models.DecimalField):
    """
    Defines a custom subclass of the decimal field
    to be uniformly used for currecny/money throughout app
    """

    def __init__(self, *args, **kwargs):
        kwargs["decimal_places"] = 2
        kwargs["max_digits"] = 18
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["decimal_places"]
        del kwargs["max_digits"]

        return name, path, args, kwargs


class CustomRateField(models.DecimalField):
    """
    Defines a custom subclass of the decimal field
    to be uniformly used for rates (e.g interest rate)
    throughout app
    """

    def __init__(self, *args, **kwargs):
        kwargs["decimal_places"] = 3
        kwargs["max_digits"] = 6
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        del kwargs["decimal_places"]
        del kwargs["max_digits"]

        return name, path, args, kwargs


class SupportedCurrencies(ModelChoiceMixin, StrEnum):
    """
    Represents supported currencies
    """

    NIGERIAN_NAIRA = "ngn"
    US_DOLLAR = "usd"

    @classmethod
    def max_name_length(cls) -> int:
        return 3


class SupportedFloatingInterestRates(ModelChoiceMixin, StrEnum):
    """
    Represents supported widely accepted floating interest rates
    """

    NIGERIAN_PRIME_LENDING_RATE = "nigerian_prime_lending_rate"

    @classmethod
    def max_name_length(cls) -> int:
        return 128
