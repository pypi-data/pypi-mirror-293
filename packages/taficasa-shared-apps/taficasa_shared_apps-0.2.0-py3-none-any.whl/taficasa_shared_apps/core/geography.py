from enum import StrEnum

from core.mixins import ModelChoiceMixin


class SupportedCountries(ModelChoiceMixin, StrEnum):
    """
    Represents supported countries
    """

    NIGERIA = "nga"

    def max_name_length(cls) -> int:
        return 16
